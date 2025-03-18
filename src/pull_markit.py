"""
Functions to pull and calculate the CDS midprice from the WRDS database.
"""
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")

# Define a mapping for column name changes over different years
COLUMN_MAPPING = {
    "date": "trade_date",
    "parspread": "spread",
    # Add more mappings if needed based on pre/post-2009 differences
}

def check_column_exists(db, table, column):
    """Check if a column exists in a WRDS table."""
    query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'"
    columns = db.raw_sql(query)["column_name"].tolist()
    return column in columns

def safe_fetch_column(db, table, column):
    """Fetch a column if it exists; otherwise, return None."""
    if check_column_exists(db, table, column):
        return f", {column}"
    return ""

def pull_markit_data(start_year=START_YEAR, end_year=END_YEAR, wrds_username=WRDS_USERNAME):
    """Fetch Markit CDS data from WRDS, ensuring column consistency across years."""
    db = wrds.Connection(wrds_username=wrds_username)
    df_list = []
    
    for year in range(int(start_year), int(end_year) + 1):
        print(f"Pulling Year {year}")
        table = f"markit.cds{year}"
        
        additional_columns = "".join([safe_fetch_column(db, table, col) for col in COLUMN_MAPPING.keys()])
        
        query = f"""
        SELECT 
            ticker,
            date AS trade_date,
            AVG(parspread) AS spread
            {additional_columns} 
        FROM {table}
        WHERE tenor = '5Y' 
        AND country = 'United States'
        AND parspread IS NOT NULL
        GROUP BY ticker, trade_date
        """
        
        new_df = db.raw_sql(query)
        new_df.rename(columns=COLUMN_MAPPING, inplace=True)
        df_list.append(new_df)
    
    db.close()
    
    df_final = pd.concat(df_list, ignore_index=True)
    df_final["trade_date"] = pd.to_datetime(df_final["trade_date"])
    return df_final

def pull_markit_sector(start_year=START_YEAR, end_year=END_YEAR, wrds_username=WRDS_USERNAME):
    """Fetch unique sector and ticker combinations for US 5Y tenor CDS."""
    db = wrds.Connection(wrds_username=wrds_username)
    df_list = []
    
    for year in range(int(start_year), int(end_year) + 1):
        table = f"markit.cds{year}"
        query = f"""
        SELECT DISTINCT ticker, sector FROM {table} WHERE tenor = '5Y' AND country = 'United States'
        """
        new_df = db.raw_sql(query)
        new_df["year"] = year
        df_list.append(new_df)
    
    db.close()
    
    if df_list:
        df_final = pd.concat(df_list, ignore_index=True).drop_duplicates(subset=["sector", "ticker"], keep="first")
        return df_final
    return pd.DataFrame()

def load_markit_data(data_dir=DATA_DIR):
    path = data_dir / "Markit_CDS.parquet"
    return pd.read_parquet(path)

def load_sector_data(data_dir=DATA_DIR):
    path = data_dir / "markit_ticker_sector_link_table.parquet"
    return pd.read_parquet(path)

def load_multiple_data(data_dir=DATA_DIR):
    df_list = []
    for year in range(int(START_YEAR), int(END_YEAR) + 1):
        filename = f"markit_cds{year}.parquet"
        path = data_dir / filename
        df_list.append(pd.read_parquet(path))
    return pd.concat(df_list, ignore_index=True)

if __name__ == "__main__":
    for year in range(int(START_YEAR), int(END_YEAR) + 1):
        df = pull_markit_data(year, year)
        filename = f"markit_cds{year}.parquet"
        df.to_parquet(DATA_DIR / filename)
    
    df_sector = pull_markit_sector()
    df_sector.to_parquet(DATA_DIR / "markit_ticker_sector_link_table.parquet")
