import pytest
from bs4 import BeautifulSoup
import pandas as pd
from pandas.testing import assert_frame_equal
import re

from service.ic3_scraper import IC3Scraper
from tests.test_files.expected_scraped_data import expected_scraped_data


@pytest.fixture
def ic3_scraper_instance():
    ic3_scraper = IC3Scraper("testing-corr-id", [2016, 2017], 3, 'configs/config.yml')
    return ic3_scraper


@pytest.fixture
def ic3_report_html():
    with open('tests/test_files/ic3_report_page_example.html', 'r') as file:
        # Read the contents of the file into a string variable
        page = file.read()
    return page


@pytest.fixture
def expected_data_json():
    return expected_scraped_data


@pytest.mark.parametrize("year, state_index, expected_url", 
                        [(2016, 14, "https://www.ic3.gov/Media/PDF/AnnualReport/2016State/StateReport.aspx?s=14"),
                         (2018, 25, "https://www.ic3.gov/Media/PDF/AnnualReport/2018State/StateReport.aspx?s=25")])
def test_replace_base_url_placeholders(ic3_scraper_instance, year, state_index, expected_url):
    prepared_url = ic3_scraper_instance._replace_base_url_placeholders(year, state_index)
    assert prepared_url == expected_url


# @pytest.mark.skip(reason="skip")
@pytest.mark.parametrize("table_caption", [("Victims by Age Group"), ("Crime Type by Victim Loss")])
def test_soup_html_to_pandas_table(ic3_scraper_instance, ic3_report_html, expected_data_json, table_caption):

    expected_data = expected_data_json[table_caption]

    excpected_df = pd.DataFrame(expected_data)

    soup = BeautifulSoup(ic3_report_html, 'html.parser')
    extracted_df = ic3_scraper_instance.soup_html_to_pandas_table(
                                        soup_html=soup,
                                        table_caption=table_caption,
                                        year=2016,
                                        state_name="Alabama",
                                        is_age_group=("Age Group" in table_caption)
                                    )

    assert_frame_equal(excpected_df, extracted_df, check_dtype=False)


def test_merge_dfs_per_year_into_one(expected_data_json):
    dfs_per_year = {}
    dfs_per_year["2016"] = {
        "ic3__crime_type_by_victim_count": 
            pd.DataFrame({
                "Age_Range": ["Under 20", "20 - 29", "30 - 39", "40 - 49", "50 - 59", "Over 60"],
                "Count": [140, 560, 661, 675, 670, 669],
                "Amount_Loss": [80752, 507699, 414557, 1150530, 2203766, 2389124],
                "year": [2016, 2016, 2016, 2016, 2016, 2016],
                "state_name": ["Alabama", "Alabama", "Alabama", "Alabama", "Alabama", "Alabama"]
            })
    }
    dfs_per_year["2017"] = {
        "ic3__crime_type_by_victim_count": 
            pd.DataFrame({
                "Age_Range": ["Under 20", "20 - 29", "30 - 39", "40 - 49", "50 - 59", "Over 60"],
                "Count": [140, 560, 661, 675, 670, 669],
                "Amount_Loss": [80752, 507699, 414557, 1150530, 2203766, 2389124],
                "year": [2017, 2017, 2017, 2017, 2017, 2017],
                "state_name": ["Alabama", "Alabama", "Alabama", "Alabama", "Alabama", "Alabama"]
            })
    }
    
    expected_merged_df = pd.DataFrame(expected_data_json["expected_merged_data"])
    merged_dfs = IC3Scraper.merge_dfs_per_year_into_one(dfs_per_year)
    
    assert_frame_equal(expected_merged_df, merged_dfs["ic3__crime_type_by_victim_count"], check_dtype=False)


@pytest.mark.parametrize("col_indexes, expected_column_types", 
                        [([1], ['object', 'int', 'object', 'object', 'object']),
                         ([1, 2], ['object', 'int', 'int', 'object', 'object']),
                         ([1, 3], ['object', 'int', 'object', 'int', 'object'])])
def test_pandas_convert_string_to_int(ic3_scraper_instance, col_indexes, expected_column_types):
    df = pd.DataFrame({
        "Age_Range": ["Under 20", "20 - 29"],
        "Count": ["140", "560"],
        "Amount_Loss": ["$80,752", "$507,699"],
        "year": ["2016", "2016"],
        "state_name": ["Alabama", "Alabama"]
    })
    result_df = ic3_scraper_instance.pandas_convert_string_to_int(df, col_indexes)
    result_df_column_types = result_df.dtypes.astype(str).tolist()
    result_df_column_types_no_digits = [re.sub('[0-9]', '', i) for i in result_df_column_types]

    assert result_df_column_types_no_digits == expected_column_types


def test_extract_ic3_state_annual_reports(requests_mock, ic3_scraper_instance, ic3_report_html, expected_data_json):

    requests_mock.get("https://www.ic3.gov/Media/PDF/AnnualReport/2016State/StateReport.aspx?s=1", text=ic3_report_html)
    result_dfs = ic3_scraper_instance.extract_ic3_state_annual_reports(2016, 1)

    excepted_results_dfs_names = ['ic3__crime_type_by_victim_count', 
                                  'ic3__crime_type_by_victim_loss', 
                                  'ic3__crime_type_by_subject_count', 
                                  'ic3__crime_type_by_subject_loss', 
                                  'ic3__victims_by_age_group']
    expected_ic3__crime_type_by_victim_loss_df = pd.DataFrame(expected_data_json["Crime Type by Victim Loss"])
    excpected_ic3__victims_by_age_group = pd.DataFrame(expected_data_json["Victims by Age Group"])
    
    assert list(result_dfs.keys()) == excepted_results_dfs_names
    assert_frame_equal(result_dfs["ic3__crime_type_by_victim_loss"], expected_ic3__crime_type_by_victim_loss_df, check_dtype=False)
    assert_frame_equal(result_dfs["ic3__victims_by_age_group"], excpected_ic3__victims_by_age_group, check_dtype=False)

