import yaml
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
from retrying import retry

from .utils.setup_logging import get_logger


class IC3Scraper:

    def __init__(self, correlation_id, years, max_state_index, config_path):
        self.correlation_id = correlation_id
        self.years = years
        self.max_state_index = max_state_index

        with open(config_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

        self.log = get_logger(
            logger_name=f"{self.__class__.__name__} from {__name__}",
            extra={
                "correlation_id": self.correlation_id,
                "years": self.years,
                "max_state_index": self.max_state_index,
                "base_webscrape_url": self.config.get("base_webscrape_url")
            }
        )

    def __getattr__(self, name):
        try:
            return self.config[name]
        except Exception as e:
            self.log.exception(f"'{type(self).__name__}' object has no attribute '{name}'. Please check the config.")
            raise

    def _replace_base_url_placeholders(self, year, state_index):
        try:
            return self.base_webscrape_url.format(year=year, state_index=state_index)
        except Exception as e:
            self.log.exception(f"Couldn't swap year and state_index for base_url '{self.base_webscrape_url}' to year: {year}, state_index: {state_index}.")
            raise

    def run(self):
        self.log.info(f"STARTING THE RUN")

        result_tables = {}

        # loop through years and state_indexes. Append extracted results to final results
        for year in self.years:
            for state_index in range(1, self.max_state_index + 1):
                extracted_tables = self.extract_ic3_state_annual_reports(year, state_index)

                # append extracted results to final results,
                for table_name in extracted_tables:
                    if table_name not in result_tables:
                        result_tables[table_name] = pd.DataFrame()
                    result_tables[table_name] = pd.concat([result_tables[table_name], extracted_tables[table_name]])
                        
        self.log.info(f"SCRAPING FINISHED SUCCESSFULLY, {len(result_tables['ic3__crime_type_by_subject_loss'])}, Extracted Tables: {list(result_tables)}")

        return result_tables

    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def extract_ic3_state_annual_reports(self, year, state_index):
        url = self._replace_base_url_placeholders(year, state_index)
        extracted_tables = {}

        self.log.info(f"Extracting data for year: {year}, state_index: {state_index}, using url: {url}")

        response = requests.get(url, timeout=20)
        if not response.ok:
            error_message = f"Bad response from url: {url}. Response status: {response.status_code}"
            self.log.error(error_message)
            raise Exception(error_message)
        
        try:
            page = response.text
            soup = BeautifulSoup(page, "html.parser")

            state_name = soup.find('option', selected=True).get_text()
        except:
            self.log.exception(f"Error occured while exporting report for year: {year}, state_index: {state_index}, from url: {url}")
            raise

        for table_name, table_caption in self.tables_mapping.items():
            extracted_tables[table_name] = self.soup_html_to_pandas_table(
                soup_html=soup,
                table_caption=table_caption,
                year=year,
                state_name=state_name,
                is_age_group=("Age Group" in table_caption)
            )

        self.log.info(f"Finished extracting data for year {year}, state_index: {state_index}, state_name: {state_name}, extracted_tables: {list(extracted_tables)}")
        return extracted_tables

    def soup_html_to_pandas_table(self, soup_html, table_caption, year, state_name, is_age_group=False):
        self.log.info(f"Converting HTML from to pandas df for {table_caption} year: {year} state_name: {state_name}")

        try:
            table = soup_html.find("caption", string=table_caption).find_parent("table")

            # create pandas table out of html
            df = pd.read_html(StringIO(str(table)))[0]

            if not is_age_group:
                # remove last 4 columns that contain comments
                df = df.iloc[:-4, :]

                # most tables are split side by side, so apend rows from last two columns to first two columns
                df1 = df.iloc[:, :2]
                df2 = df.iloc[:, 2:]
                df2.columns = df1.columns 
                df = pd.concat([df1, df2], ignore_index=True)

                # remove null columns
                df = df[df.iloc[:, 1].notna()]

                df = self.pandas_convert_string_to_int(df, [1])
            else:
                # only for 'Age Group' table we have to convert two columns.
                df = df = self.pandas_convert_string_to_int(df, [1, 2])

            # add year and state_name columns
            df["year"] = year
            df["state_name"] = state_name

            # change column names so that it's _ instead of space
            df = df.rename(columns=lambda x: x.replace(' ', '_'))
        except:
            self.log.exception(f"Error occured while converting HTML to pandas for table '{table_caption}'")
            raise

        self.log.info(f"Converted HTML to pandas for {table_caption} year: {year} state_name: {state_name}, Extracted columns: {df.columns},  Extracted Rows: {len(df)}")

        return df        

    def pandas_convert_string_to_int(self, df, col_indexes):
        # change columns to integers for columns with passed indexes
        for col_index in col_indexes:
            try:
                df[df.columns[col_index]] = df[df.columns[col_index]].replace('[\$,]', '', regex=True).astype(int)
            except Exception as e:
                self.log.exception(f"Column '{df.columns[col_index]}' at col_index {col_index} cannot be converted to int.")

        return df

    @staticmethod
    def merge_dfs_per_year_into_one(result_tables_per_year):
        result_tables = {}
        for extracted_tables in result_tables_per_year.values():
            for table_name, df in extracted_tables.items():
                if table_name not in result_tables:
                    result_tables[table_name] = pd.DataFrame()

                result_tables[table_name] = pd.concat([result_tables[table_name], df], ignore_index=True)

        return result_tables
