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
    """
    Pulls the Markit CDS spread data from the WRDS database.
    Args:
        start_year (str): The starting year of the data to pull. Defaults to START_YEAR.
        end_year (str): The ending year of the data to pull. Defaults to END_YEAR.
        wrds_username (str): The WRDS username for database authentication.

    Returns:
        pd.DataFrame: A DataFrame containing the following columns:
            - `ticker` (str): The stock ticker of the company.
            - `redcode` (str): The RED code (Markit identifier) for the entity.
            - `month` (datetime): The first day of the month for which the data is aggregated.
            - `first_trade_date` (datetime): The earliest trade date for the given month.
            - `midspread` (float): The average 5-year CDS spread (in basis points) for that month.
    """
    db = wrds.Connection(wrds_username = wrds_username)
    df = pd.DataFrame()

    for year in range(int(start_year), int(end_year)):
        table = f"markit.cds{year}"
        query=f"""
        SELECT 
            ticker, redcode, DATE_TRUNC('month', date) AS month, MIN(date) AS first_trade_date, AVG(parspread) AS midspread
        FROM 
            {table}
        WHERE 
            tenor = '5Y' AND country = 'United States'
        GROUP BY 
            month, ticker, redcode
        """
        new_df = db.raw_sql(query)
        df = pd.concat([df, new_df])

    db.close()
    return df


if __name__ == "__main__":
    df = pull_markit_data()
    df.to_parquet(DATA_DIR / "Markit_CDS.parquet")

