from service.ic3_scraper import IC3Scraper
from service.utils.setup_logging import setup_logging
from service.exporter import Exporter

import threading
import yaml
import uuid


def get_run_variables(config_path):
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    start_year = config.get("start_year")
    end_year = config.get("end_year")
    years = [year for year in range(start_year, end_year + 1) if 2016 <= year <= 2023]

    max_state_index = config.get("max_state_index")
    output_path = config.get("output_path")

    return years, max_state_index, output_path


if __name__ == "__main__":
    setup_logging("logs/logs.log")

    config_path = 'configs/config.yml'

    # get run variables from config file
    years, max_state_index, output_path = get_run_variables(config_path)

    threads = []
    result_tables_per_year = {}
    uuid1 = uuid.uuid1()

    # run each year in different thread, this way it runs faster...
    for year in years:
        correlation_id = f"corr-id-thread-for-year-{year}-{uuid1}"
        scraper = IC3Scraper(correlation_id, [year], max_state_index, config_path)

        thread = threading.Thread(target=lambda key=year: result_tables_per_year.update({key: scraper.run()}))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # join results from different threads into one
    result_tables = IC3Scraper.merge_dfs_per_year_into_one(result_tables_per_year)

    # export results
    exporter = Exporter(f"corr-id-{uuid1}", config_path)
    for table_name, df in result_tables.items():
        exporter.export_pandas_to_postgres(df, table_name)
        exporter.export_pandas_to_parquet(df, f"{output_path}/{table_name}")

