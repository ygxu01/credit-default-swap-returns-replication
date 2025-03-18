"""
Test suite for the `pull_markit` module to validate correct data fetching and structure:

1. `test_pull_markit_data`: Ensures that the `pull_markit_data` function pulls the correct Markit data, returns a pandas DataFrame, and contains the expected columns. This test does not check the correctness of data content but ensures the function runs without errors and returns the expected format.
2. `test_pull_market_sector`: Verifies that the `pull_markit_sector` function retrieves sector data correctly, returns a pandas DataFrame with the expected columns, and matches known characteristics like the number of unique sectors and the total rows in the dataset. It also tests the `load_sector_data` function for data completeness.

These tests are important for confirming the correct functionality of data retrieval functions and ensuring that the resulting data is structured as expected, reducing the risk of errors downstream in the analysis pipeline.
"""


import pandas as pd
from pathlib import Path
from settings import config
import pull_markit

# Get DATA_DIR from settings
DATA_DIR = Path(config("DATA_DIR"))
MANUAL_DATA_DIR = Path(config("MANUAL_DATA_DIR"))


def test_pull_markit_data():
    """Test pulling Markit data.""" 
    # since it takes a long time to pull the data, we will just test if the function runs without error
    df = pull_markit.pull_markit_data("2001","2001")

     # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame has the expected columns
    expected_columns = ["ticker","trade_date", "spread"]
    assert all(col in df.columns for col in expected_columns)


def test_pull_market_sector():
    """Test pulling Markit sector data.""" 
    # since it takes a long time to pull the data, we will just test if the function runs without error
    df = pull_markit.pull_markit_sector("2001","2001")

     # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame has the expected columns
    expected_columns = ["ticker","sector"]
    assert all(col in df.columns for col in expected_columns)

    df = pull_markit.load_sector_data()

    assert(len(df) == 2292)
    assert(df["sector"].nunique() == 11)


    