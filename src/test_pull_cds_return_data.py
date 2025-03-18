"""
Test suite for the `pull_cds_return_data` module to ensure correct data loading and transformation:
1. `test_pull_real_cds_return`: Verifies that the `pull_real_cds_return` function correctly loads the dataset, includes the expected columns, and does not contain missing values.
2. `test_unpivot_table`: Ensures that the `unpivot_table` function correctly reshapes the data and that the resulting `yyyymm` values are within the expected date range.

These tests are crucial for validating data processing pipelines to ensure that data is loaded, transformed, and presented in the correct format.
"""


import datetime
import pandas as pd
from pathlib import Path
from settings import config
import pull_cds_return_data

# Get DATA_DIR from settings
DATA_DIR = Path(config("DATA_DIR"))
MANUAL_DATA_DIR = Path(config("MANUAL_DATA_DIR"))


def test_pull_real_cds_return():
    """Test if pull_real_cds_return correctly loads and processes the dataset."""
    df = pull_cds_return_data.pull_real_cds_return()

    # Ensure it's a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Ensure expected columns are present
    expected_columns = [f"CDS_{i:02d}" for i in range(1, 21)]
    assert all(col in df.columns for col in expected_columns)

    # Ensure no missing values after dropping NaNs
    assert df.isna().sum().sum() == 0

def test_unpivot_table():
    df = pull_cds_return_data.load_real_cds_return()
    df_unpivoted = pull_cds_return_data.unpivot_table(df)

    assert df_unpivoted["yyyymm"].min() == datetime.date(2001, 2, 1)
    assert df_unpivoted["yyyymm"].max() == datetime.date(2012,12,1)
