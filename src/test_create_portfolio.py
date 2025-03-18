"""Test suite for validating functions related to portfolio creation, including month assignment, 
monthly return computation, portfolio construction, and reshaping data into wide format."""

import pandas as pd
from pathlib import Path

from create_portfolio import *

from settings import config

DATA_DIR = Path(config("DATA_DIR"))


def test_create_yyyymm_col():
    """
    Test that create_yyyymm_col correctly assigns YYYYMM values to trade dates. 
    """
    input_df = pd.DataFrame(
        {
            "trade_date": pd.to_datetime(["2023-01-15", "2023-02-20", "2023-03-10"]),
        }
    )

    expected_output = input_df.copy()
    expected_output["yyyymm"] = [202301, 202302, 202303]
    expected_output["yyyymm"] = expected_output["yyyymm"].astype(int)  # Ensure int64 type

    output_df = create_yyyymm_col(input_df)
    output_df["yyyymm"] = output_df["yyyymm"].astype(int)  # Cast to int64 to match expected

    pd.testing.assert_frame_equal(output_df, expected_output)

def test_calc_cds_monthly_return():
    """
    Test that calc_cds_monthly_return correctly computes compounded monthly returns.
    """
    input_df = pd.DataFrame(
        {
            "ticker": ["A", "A", "A", "B", "B"],
            "trade_date": pd.to_datetime(
                ["2023-01-01", "2023-01-02", "2023-01-03", "2023-02-01", "2023-02-02"]
            ),
            "yyyymm": [202301, 202301, 202301, 202302, 202302],
            "daily_return": [0.01, 0.02, -0.01, 0.015, -0.005],
        }
    )

    expected_output = pd.DataFrame(
        {
            "ticker": ["A", "B"],
            "yyyymm": [202301, 202302],
            "daily_return": [(1.01 * 1.02 * 0.99) - 1, (1.015 * 0.995) - 1],
        }
    )

    output_df = calc_cds_monthly_return(input_df)
    pd.testing.assert_frame_equal(output_df, expected_output, check_dtype=False)



def test_construct_cds_portfolios():
    """
    Test that construct_cds_portfolios assigns tickers into 20 quantile portfolios based on their spread.
    """
    monthly_returns = pd.DataFrame(
        {
            "ticker": ["A", "B", "C", "D"],
            "yyyymm": [202301, 202301, 202301, 202301],
            "daily_return": [0.02, -0.01, 0.015, 0.03],
        }
    )

    rd_df = pd.DataFrame(
        {
            "ticker": ["A", "B", "C", "D"],
            "yyyymm": [202301, 202301, 202301, 202301],
            "spread": [10, 50, 20, 5],  # Spread ranks: D (1), A (2), C (3), B (4)
        }
    )

    output_df = construct_cds_portfolios(monthly_returns, rd_df)

    assert "portfolio" in output_df.columns
    assert output_df["portfolio"].nunique() > 1  # Ensure sorting into groups is occurring


def test_pivot_table():
    """
    Test that pivot_table correctly reshapes data into a wide format with CDS portfolio columns.
    """
    input_df = pd.DataFrame(
        {
            "yyyymm": [202301, 202301, 202301, 202302, 202302],
            "portfolio": [1, 2, 3, 1, 2],
            "daily_return": [0.01, -0.02, 0.03, 0.015, -0.01],
        }
    )

    expected_output = pd.DataFrame(
        {
            "CDS_01": [0.01, 0.015],
            "CDS_02": [-0.02, -0.01],
            "CDS_03": [0.03, None],
        },
        index=[202301, 202302],
    )

    expected_output.index.name = "yyyymm"

    output_df = pivot_table(input_df)
    pd.testing.assert_frame_equal(output_df, expected_output, check_dtype=False)
