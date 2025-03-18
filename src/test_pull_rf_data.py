import pytest
import pandas as pd
from pathlib import Path
from settings import config
import pull_cds_return_data
import pull_markit
import pull_rf_data

# Get DATA_DIR from settings
DATA_DIR = Path(config("DATA_DIR"))
MANUAL_DATA_DIR = Path(config("MANUAL_DATA_DIR"))


def test_pull_fed_yield_curve():
    """Test pulling Federal Reserve yield curve data."""
    df = pull_rf_data.pull_fed_yield_curve()

    # Ensure it's a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Ensure expected columns exist
    expected_columns = ["SVENY01", "SVENY02", "SVENY03", "SVENY04", "SVENY05"]
    assert all(col in df.columns for col in expected_columns)

    # Ensure no missing values
    assert df.isna().sum().sum() == 0


def test_pull_swap_rates():
    """Test pulling swap rates data from FRED."""
    df = pull_rf_data.pull_swap_rates()

    # Ensure it's a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Ensure required columns exist
    expected_columns = ["DGS3MO", "DGS6MO"]
    assert all(col in df.columns for col in expected_columns)


