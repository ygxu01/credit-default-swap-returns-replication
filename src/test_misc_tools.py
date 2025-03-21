"""
Test suite for utility functions to ensure correct functionality of date conversions and data retrieval:
1. `test_generate_month_code`: Verifies the correct conversion of a date to a YYYYMM format.
2. `test_month_code_to_date`: Ensures proper conversion from YYYYMM to a `datetime.date` object.
3. `test_pull_from_wrds`: Confirms that data retrieval from WRDS returns a pandas DataFrame.

These tests help ensure the correctness and reliability of date-related transformations and data retrieval logic.
"""


import pandas as pd
import datetime
from misc_tools import *

def test_generate_month_code():
    """
    Test generate_month_code() to ensure correct YYYYMM conversion.
    """
    assert generate_month_code(datetime.date(2024, 5, 1)) == 202405
    assert generate_month_code(datetime.date(1999, 12, 1)) == 199912
    assert generate_month_code(datetime.date(2000, 1, 15)) == 200001


def test_month_code_to_date():
    """
    Test month_code_to_date() to ensure proper conversion from YYYYMM to datetime.date.
    """
    assert month_code_to_date(202405) == datetime.date(2024, 5, 1)
    assert month_code_to_date(199912) == datetime.date(1999, 12, 1)
    assert month_code_to_date(200001) == datetime.date(2000, 1, 1)



def test_pull_from_wrds():
    """
    Test pull_from_wrds() to check if it returns a DataFrame.
    """
    query = "SELECT * FROM markit.cds2001 LIMIT 5"
    df = pull_from_wrds(query)
    
    assert isinstance(df, pd.DataFrame)
