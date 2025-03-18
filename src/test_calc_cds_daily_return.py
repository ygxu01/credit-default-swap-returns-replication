import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
import datetime

from calc_cds_daily_return import *

from settings import config

DATA_DIR = config("DATA_DIR")


def test_calc_risk_free_rate():
    """
    Given a risk-free dataset with specific yields at fixed tenors,
    we apply cubic spline interpolation to generate interpolated rates.

    Consider the input:

    - Maturity 0.25 years: 0.01
    - Maturity 0.5 years: 0.015
    - Maturity 1 year: 0.02
    - Maturity 2 years: 0.025
    - Maturity 3 years: 0.03
    - Maturity 4 years: 0.035
    - Maturity 5 years: 0.04

    The output should have interpolated rates across 60 evenly spaced points.
    """
    input_data = pd.DataFrame(
        data={
            "Date": pd.to_datetime(["2022-01-01"]),
            0.25: [0.01],
            0.5: [0.015],
            1: [0.02],
            2: [0.025],
            3: [0.03],
            4: [0.035],
            5: [0.04],
        }
    ).set_index("Date")

    output = calc_risk_free_rate(input_data)

    assert isinstance(output, pd.DataFrame)
    assert output.shape[1] == 60  
    assert not output.isnull().values.any()  


def test_calc_lambda():
    """
    The lambda parameter (hazard rate) is calculated using the CDS spread and
    loss-given-default assumption (L). 

    Given a CDS spread of 100bps and L = 0.6, lambda should be:
    lambda = 12 * log(1 + spread / (12 * L))
    """
    input_data = pd.DataFrame(
        data={
            "trade_date": pd.to_datetime(["2022-01-01"]),
            "spread": [100],  # 100bps CDS spread
        }
    )

    output = calc_lambda(input_data, L=0.6)

    assert "lambda" in output.columns
    assert (output["lambda"] > 0).all()


def test_calc_risk_free_term():
    """
    The risk-free discount factor should be computed using the formula:

    DF(t) = exp(-r_t * t / 12)
    """
    input_data = pd.DataFrame(
        data={
            "Date": pd.to_datetime(["2022-01-01"]),
            0.25: [0.01],
            0.5: [0.015],
            1: [0.02],
            2: [0.025],
            3: [0.03],
            4: [0.035],
            5: [0.04],
        }
    ).set_index("Date")

    output = calc_risk_free_term(input_data)

    assert isinstance(output, pd.DataFrame)
    assert (output.values <= 1).all()  # Discount factors should be ≤ 1
    assert (output.values > 0).all()  # Discount factors should be positive


def test_calc_cds_daily_return():
    """
    Computes CDS daily return using the formula:

    daily_return = -(spread_prev / 250 + (spread - spread_prev) * RD_prev)
    """
    input_data = pd.DataFrame(
        data={
            "trade_date": pd.to_datetime(["2022-01-01", "2022-02-01"]),
            "ticker": ["A", "A"],
            "spread": [100, 110],
            "spread_prev": [95, 100],
            "RD": [0.02, 0.025],
            "RD_prev": [0.015, 0.02],
        }
    )

    output = calc_cds_daily_return(input_data)

    assert isinstance(output, pd.DataFrame)
    assert "daily_return" in output.columns
    assert not output["daily_return"].isnull().any()

