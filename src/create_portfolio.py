from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path

import numpy as np
import pandas as pd
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")

from calc_cds_t_return import load_cds_return

def generate_month_code(date):
    year = date.year
    month = date.month

    if month > 10:
        return f"{year}{month}"
    else:
        return f"{year}0{month}"


def construct_cds_portfolios(cds_df, num_portfolios=20):
    """
    Constructs CDS portfolios by sorting firms into equal-sized portfolios 
    each month based on their CDS spreads.

    Args:
        cds_df (pd.DataFrame): DataFrame with 'ticker', 'month', 'spread'.
        num_portfolios (int): Number of portfolios (default = 20).

    Returns:
        pd.DataFrame: Portfolio assignment for each firm by month.
    """
    # Rank firms by CDS spread each month
    cds_df["spread_rank"] = cds_df.groupby("month_code")["spread"].rank(method="first")

    # Assign firms into portfolios (1 = lowest spreads, num_portfolios = highest spreads)
    cds_df["portfolio"] = cds_df.groupby("month_code")["spread"].transform(
        lambda x: pd.qcut(x, num_portfolios, labels=False) + 1
    )

    return cds_df[["ticker", "month_code", "spread", "portfolio", "return"]]


def calc_avg_portfolio_return(portfolio_df):
    """
    Computes the average return for each CDS portfolio per month.

    Args:
        portfolio_df (pd.DataFrame): DataFrame with 'month', 'portfolio', 'return'.

    Returns:
        pd.DataFrame: Portfolio-level average returns per month.
    """
    # Compute equal-weighted average return per portfolio each month
    portfolio_avg_return = portfolio_df.groupby(["month_code", "portfolio"])["return"].mean().reset_index()

    return portfolio_avg_return