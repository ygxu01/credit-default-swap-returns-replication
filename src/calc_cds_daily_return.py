"""
Functions for processing CDS and risk-free rate data, including interpolation, 
calculating risk-free rates, default probabilities, and CDS daily returns.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

from pathlib import Path
from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")

from pull_markit import load_markit_data, load_multiple_data, load_sector_data
from pull_interest_rates_data import load_fed_yield_curve, load_fred_data


def merge_rf_data(fed_data, fred_data, markit):
    """
    Merge Fed and FRED risk-free rate data with Markit trade dates.
    """
    rf_data = pd.merge(fred_data, fed_data, on="Date")
    rf_data = rf_data.merge(
        markit["trade_date"].drop_duplicates(), left_on="Date", right_on="trade_date", how="inner"
    ).set_index("trade_date")
    rf_data.index.name = "Date"
    return rf_data


def filter_sector(markit, sector_df):
    """
    (optional, the paper didn't mention such filtering)
    Filter out financial and government sectors from Markit data.
    """
    markit = pd.merge(markit, sector_df, on="ticker", how="left")
    markit = markit[(markit["sector"] != "Financials") & (markit["sector"] != "Government")]
    return markit


def interpolate_row(y):
    """
    Apply cubic spline interpolation to yield curve data.
    """
    x = [0.25, 0.5, 1, 2, 3, 4, 5]
    xvals = np.linspace(1 / 12, 5, 60)
    f = CubicSpline(x, y, bc_type="natural")  
    return pd.Series(f(xvals), index=xvals)  


def calc_risk_free_rate(rf_data):
    """
    Calculate interpolated risk-free rates for multiple maturities.
    """
    xvals = np.linspace(1 / 12, 5, 60)
    r_t_df = pd.DataFrame(index=rf_data.index, columns=xvals)
    r_t_df.loc[:, :] = rf_data.apply(interpolate_row, axis=1)
    return r_t_df.astype(float)


def calc_lambda(cds_df, L=0.6):
    """
    Calculate default intensity (lambda) using CDS spreads.
    """
    cds_df["lambda"] = 12 * np.log(1 + cds_df["spread"] / (12 * L))
    return cds_df


def calc_risk_free_term(rf_data):
    """
    Compute risk-free discount factors.
    """
    r_t_df = calc_risk_free_rate(rf_data)
    maturities = np.array(r_t_df.columns, dtype=float)
    for i in range(len(r_t_df)):
        r_t_df.iloc[i] *= maturities
    r_t_df = np.exp(-1 * r_t_df / 12)
    return r_t_df


def calc_RD(cds_df, r_t_df, maturity=5):
    """
    Compute risk-neutral default probability RD.
    """
    cds_df["trade_date"] = pd.to_datetime(cds_df["trade_date"])

    rd_df = r_t_df.merge(cds_df, right_on="trade_date", left_on=r_t_df.index, how="right")
    rd_df = calc_lambda(rd_df)
    rd_df = rd_df.dropna(axis=0)

    rd_df["RD"] = 0
    for j in range(1, 12 * maturity + 1):  
        risk_free_col = rd_df.iloc[:, j - 1]
        rd_df["RD"] += np.exp(-j / 12 * rd_df["lambda"]) * risk_free_col
    rd_df["RD"] /= 12

    rd_df = rd_df.sort_values(["ticker", "trade_date"])
    rd_df["RD_prev"] = rd_df.groupby("ticker")["RD"].shift(1)
    rd_df["spread_prev"] = rd_df.groupby("ticker")["spread"].shift(1)

    columns_available = [
        col for col in ["ticker", "trade_date", "spread_prev", "spread", "RD", "RD_prev", "sector"]
        if col in rd_df.columns
    ]
    return rd_df[columns_available]


def calc_cds_daily_return(rd_df):
    """
    Compute daily CDS return based on spread changes and RD.
    """
    rd_df["daily_return"] = -(
        rd_df["spread_prev"] / 250 + (rd_df["spread"] - rd_df["spread_prev"]) * rd_df["RD_prev"]
    )
    rd_df = rd_df.dropna(subset=["daily_return"])
    return rd_df


def load_cds_return(data_dir=DATA_DIR):
    """
    Load precomputed CDS daily returns.
    """
    path = data_dir / "CDS_daily_return.parquet"
    return pd.read_parquet(path)


if __name__ == "__main__":
    path = DATA_DIR / "Markit_CDS.parquet"
    if path.exists():
        markit = load_markit_data()
    else:
        markit = load_multiple_data()

    sector_df = load_sector_data()

    fed_data = load_fed_yield_curve()
    fred_data = load_fred_data()

    rf_data = merge_rf_data(fed_data, fred_data, markit)
    risk_free_term_df = calc_risk_free_term(rf_data)

    rd_df = calc_RD(markit, risk_free_term_df)
    final_df = calc_cds_daily_return(rd_df)

    final_df.to_parquet(DATA_DIR / "CDS_daily_return.parquet")
