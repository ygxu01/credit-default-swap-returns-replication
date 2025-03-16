from pathlib import Path

import numpy as np
import pandas as pd

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")

from calc_cds_daily_return import load_cds_return
from misc_tools import generate_month_code
    

def create_yyyymm_col(daily_rd_df):
    daily_rd_df["yyyymm"] = daily_rd_df["trade_date"].apply(generate_month_code)
    return daily_rd_df


def calc_cds_monthly_return(daily_rd_df):
    """
    Compute the monthly return by compounding daily returns:
    (1 + Monthly Return) = Π (1 + Daily Return)
    """
    # Aggregate daily returns into monthly compounded returns
    monthly_returns = (
        daily_rd_df.groupby(["ticker", "yyyymm"])["daily_return"]
        .apply(lambda x: (x + 1).prod() - 1)  # Compounding formula
        .reset_index()
    )

    return monthly_returns

def construct_cds_portfolios(monthly_returns, rd_df):
    """
    Construct 20 portfolios sorted by the first trading day's CDS spread.
    """
    # Get the first trading day of each month
    first_day_spread = rd_df.groupby(["ticker", "yyyymm"]).first()["spread"].reset_index()

    # Rank tickers into 20 portfolios based on spread
    first_day_spread["portfolio"] = first_day_spread.groupby("yyyymm")["spread"].transform(
        lambda x: pd.qcut(x, 20, labels=False) + 1  
    )

    # Merge portfolio assignments into monthly returns
    portfolio_returns = monthly_returns.merge(first_day_spread[["ticker", "yyyymm", "portfolio"]], on=["ticker", "yyyymm"])

    # Compute value-weighted portfolio returns
    final_portfolio_returns = portfolio_returns.groupby(["yyyymm", "portfolio"])["daily_return"].mean().reset_index()

    return final_portfolio_returns


def pivot_table(portfolio):
    df_pivot = portfolio.pivot(index='yyyymm', columns='portfolio', values='daily_return')
    df_pivot.columns = [f"CDS_{str(col).zfill(2)}" for col in df_pivot.columns]
    return df_pivot


def load_portfolio(data_dir=DATA_DIR):
    path = data_dir / "portfolio_return.parquet" 
    _df = pd.read_parquet(path)
    return _df


if __name__ == "__main__":
    daily_return_df = load_cds_return()

    daily_return_df = create_yyyymm_col(daily_return_df)

    monthly_return_df = calc_cds_monthly_return(daily_return_df)

    portfolio = construct_cds_portfolios(monthly_return_df,daily_return_df)

    portfolio.to_parquet(DATA_DIR / "portfolio_return.parquet")


