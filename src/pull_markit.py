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
    df = pd.DataFrame()

    for year in range(int(start_year), int(end_year) + 1):
        print(f"Pulling Year {year}")  
        table = f"markit.cds{year}"
        query = f"""
        SELECT 
            ticker, 
            date AS trade_date,  
            AVG(parspread) AS spread
        FROM {table}
        WHERE tenor = '5Y' 
        AND country = 'United States'
        AND parspread IS NOT NULL
        GROUP BY ticker, trade_date
        """
        new_df = db.raw_sql(query)
        df = pd.concat([df, new_df])

    db.close()
    df["trade_date"] = pd.to_datetime(df["trade_date"])

    return df


def load_markit_data(data_dir=DATA_DIR):
    path = data_dir / "Markit_CDS.parquet"
    _df = pd.read_parquet(path)
    return _df


def load_multiple_data(data_dir=DATA_DIR):
    _df_final = pd.DataFrame()
    for year in range(int(START_YEAR), int(END_YEAR) + 1):
        filename = f"markit_cds{year}.parquet"
        path = data_dir / filename
        _df = pd.read_parquet(path)
        _df_final = pd.concat([_df,_df_final])
    return _df_final


if __name__ == "__main__":
    for year in range(int(START_YEAR), int(END_YEAR) + 1):
        df = pull_markit_data(year, year)
        filename = f"markit_cds{year}.parquet"
        df.to_parquet(DATA_DIR / filename)

