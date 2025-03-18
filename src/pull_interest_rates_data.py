"""
This file aims to define functions to clean and merge data releated to risk-free rate construction.
"""

import pandas as pd
import requests
from io import BytesIO
from pathlib import Path
import settings
import io

from settings import config


DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")

def pull_fed_yield_curve(start_year = START_YEAR):
    """
    Download the latest yield curve from the Federal Reserve
    
    This is the published data using Gurkaynak, Sack, and Wright (2007) model
    """
    
    url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628.csv"
    response = requests.get(url)
    pdf_stream = BytesIO(response.content)
    df = pd.read_csv(pdf_stream, skiprows=9, index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    df = df[start_year:]
    df = df.dropna(axis=0)
    df = df/100
    cols = ['SVENY' + str(i).zfill(2) for i in range(1, 6)]
    return df[cols]

    
def pull_swap_rates(start_year = START_YEAR):
    urls = {
        "DGS6MO": "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=803&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DGS6MO&scale=left&cosd=1981-09-01&coed=2025-03-12&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-03-14&revision_date=2025-03-14&nd=1981-09-01",
        "DGS3MO": "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23ebf3fb&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=803&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DGS3MO&scale=left&cosd=1981-09-01&coed=2025-03-12&line_color=%230073e6&link_values=false&line_style=solid&mark_type=none&mw=3&lw=3&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2025-03-14&revision_date=2025-03-14&nd=1981-09-01"
    }

    dataframes = {}
    for key, url in urls.items():
        response = requests.get(url)
        response.raise_for_status()  
        
        df = pd.read_csv(io.StringIO(response.text), parse_dates=["observation_date"])
        df.columns = ["observation_date", key]  
        dataframes[key] = df

    # Merge dataframes on DATE
    df_merged = dataframes["DGS3MO"].merge(dataframes["DGS6MO"], on="observation_date", how="outer")
    df_merged = df_merged.rename(columns = {"observation_date": "Date"})
    df_merged = df_merged.set_index("Date")
    df_merged = df_merged[start_year:]
    df_merged = df_merged.dropna(axis=0)
    df_merged = df_merged / 100
    return df_merged


def load_fed_yield_curve(data_dir=DATA_DIR):
    path = data_dir  / "fed_yield_curve.parquet"
    _df = pd.read_parquet(path)
    return _df

def load_fred_data(data_dir=DATA_DIR):
    path = data_dir  / "swap_rates.parquet"
    _df = pd.read_parquet(path)
    return _df



if __name__ == "__main__":
    df = pull_fed_yield_curve()
    path = Path(DATA_DIR) / "fed_yield_curve.parquet"
    df.to_parquet(path)

    df_fred = pull_swap_rates()
    path_fred = Path(DATA_DIR) / "swap_rates.parquet"
    df_fred.to_parquet(path_fred)
    
