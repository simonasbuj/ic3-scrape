import yaml
import sqlalchemy
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.schema import CreateSchema
import pandas as pd

from .utils.setup_logging import get_logger


class Exporter:

    def __init__(self, correlation_id, config_path):
        with open(config_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)
        
        self.log = get_logger(
            logger_name=f"{self.__class__.__name__} from {__name__}",
            extra={
                "correlation_id": correlation_id
            }
        )

    def __getattr__(self, name):
        try:
            return self.config[name]
        except Exception as e:
            self.log.exception(f"'{type(self).__name__}' object has no attribute '{name}'. Please check the config.")
            raise

    def export_pandas_to_postgres(self, df, table_name):
        self.log.info(f"Starting exporting to postgres. table_name: {table_name}, df_cols: {df.columns}, rows: {len(df)}")
        
        schema = self.postgres_db.get("schema")

        df.columns = df.columns.str.lower()
        df["inserted_at"] = pd.Timestamp.now()

        try:
            with self._get_postgres_conn_engine().connect() as conn:
                conn.execute(CreateSchema(schema, if_not_exists=True))
                df.to_sql(table_name, conn, schema=schema, if_exists="replace", index=False)
                conn.commit()

                self.log.info(f"Successfully exported to postgres. table_name: {table_name}, df_cols: {df.columns}, rows: {len(df)}")
        except Exception as e:
            self.log.exception(f"Exporting to postgres failed. table_name: {table_name}, df_cols: {df.columns}, rows: {len(df)}")

    def export_pandas_to_parquet(self, df, output_path):

        partitions = self.config.get("partitions")

        self.log.info(f"Starting exporting to parquet. output_path: {output_path}, partitions: {partitions}, df_cols: {df.columns}, rows: {len(df)}")

        try:
            df.to_parquet(path=output_path, partition_cols=partitions, index=False)
            self.log.info(f"Succesfully exported to parquet. output_path: {output_path}, partitions: {partitions}, df_cols: {df.columns}, rows: {len(df)}")
        except:
            self.log.exception("Exporting to parquet failed")

    def _get_postgres_conn_engine(self):
        host = self.postgres_db.get("host")
        port = self.postgres_db.get("port")
        database = self.postgres_db.get("database")
        user = self.postgres_db.get("user")
        password = self.postgres_db.get("password")
        
        self.log.info(f"Getting Postgres Connection. host: {host}, port: {port}, database: {database}, user: {user}")

        conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

        return create_engine(conn_string)

    def _delete_old_data(self, df, schema, table_name):
        
        years_and_states = df[["year", "state_name"]].drop_duplicates().to_dict(orient='records')

        conditions = []
        for item in years_and_states:
            condition = f"(year = {item['year']} and state_name = '{item['state_name']}')"
            conditions.append(condition)

        delete_sql = f"""
            DELETE FROM {schema}.{table_name}
            WHERE 
                {' or '.join(conditions)}
        """

        self.log.info(f"Deleting data from {schema}.{table_name}, for these condition groups: {conditions}")
        try:
            with self._get_postgres_conn_engine().connect() as conn:
                conn.execute(text(delete_sql))
                conn.commit()
        except Exception as e:
            self.log.exception(f"Error occured while deleting data from {schema}.{table_name}, for these condition groups: {conditions}")
