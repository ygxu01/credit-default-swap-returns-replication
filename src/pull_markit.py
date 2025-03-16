"""
Functions to pull and calculate the CDS midprice from the WRDS database.
"""
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


def pull_markit_data(start_year=START_YEAR, end_year=END_YEAR, wrds_username=WRDS_USERNAME):
    db = wrds.Connection(wrds_username=wrds_username)
    first_trade_df = pd.DataFrame()
    last_trade_df = pd.DataFrame()

    for year in range(int(start_year), int(end_year)):
        table = f"markit.cds{year}"
        query = f"""
        WITH trade_data AS (
            SELECT 
                ticker, 
                redcode, 
                DATE_TRUNC('month', date) AS month,  
                date AS trade_date, 
                parspread AS midspread,
                ROW_NUMBER() OVER (
                    PARTITION BY ticker, redcode, DATE_TRUNC('month', date) 
                    ORDER BY date ASC
                ) AS first_trade_rank,  -- Rank 1 for first trade
                ROW_NUMBER() OVER (
                    PARTITION BY ticker, redcode, DATE_TRUNC('month', date) 
                    ORDER BY date DESC
                ) AS last_trade_rank  -- Rank 1 for last trade
            FROM 
                {table}
            WHERE 
                tenor = '5Y' 
                AND country = 'United States'
        )
        SELECT 
            ticker, 
            redcode, 
            month, 
            trade_date, 
            midspread,
            CASE WHEN first_trade_rank = 1 THEN 'first' ELSE 'last' END AS trade_type
        FROM 
            trade_data
        WHERE 
            first_trade_rank = 1 OR last_trade_rank = 1
        """
        new_df = db.raw_sql(query)

        # Split into first and last trade datasets
        first_trades = new_df[new_df['trade_type'] == 'first'].drop(columns=['trade_type'])
        last_trades = new_df[new_df['trade_type'] == 'last'].drop(columns=['trade_type'])

        # Combine data across years
        first_trade_df = pd.concat([first_trade_df, first_trades])
        last_trade_df = pd.concat([last_trade_df, last_trades])

    db.close()

    # Ensure date columns are in datetime format
    first_trade_df['trade_date'] = pd.to_datetime(first_trade_df['trade_date'])
    last_trade_df['trade_date'] = pd.to_datetime(last_trade_df['trade_date'])

    return first_trade_df, last_trade_df


def merge_first_last_trades(first_trade_df, last_trade_df):
    """
    Merge first trade data of the current month with the last trade data of the previous month.
    """
    first_trade_df = first_trade_df.sort_values(by=["ticker", "redcode", "month"])
    last_trade_df = last_trade_df.sort_values(by=["ticker", "redcode", "month"])
    last_trade_df["merge_month"] = last_trade_df["month"].shift(-1)
    merged_df = first_trade_df.merge(last_trade_df[["ticker","merge_month","midspread"]], how = "left", right_on=["ticker","merge_month"], left_on = ["ticker","month"])
    merged_df = merged_df.rename(columns = {"midspread_x": "spread", "midspread_y":"prev_spread"})
    merged_df = merged_df[["ticker","month","trade_date","spread","prev_spread"]]
    return merged_df

# Run merging function

def load_markit_data(data_dir=DATA_DIR):
    path = data_dir / "Markit_CDS.parquet"
    _df = pd.read_parquet(path)
    return _df


if __name__ == "__main__":
    first_trade_df, last_trade_df = pull_markit_data()
    merged_df = merge_first_last_trades(first_trade_df, last_trade_df)

    merged_df.to_parquet(DATA_DIR / "Markit_CDS.parquet")

