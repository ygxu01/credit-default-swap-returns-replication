"""
This module contains functions to pull and load the records of primary dealers
(1960-2014) from the NY Fed website.
https://www.newyorkfed.org/markets/primarydealers#primary-dealers 

Also, cleaning and merging functions are included to make the table mergeable 
for Compustat datasets.
"""

import pandas as pd
from pathlib import Path
from settings import config


DATA_DIR = config("DATA_DIR")
print("Data Directory:", DATA_DIR)

def pull_nyfed_dealers():
    """
    Download the primary dealer records from NY Fed.

    For this project, we only need the "Dealer Alpha Sheet" which contains the list 
    of primary dealers from 1960-2014 and their start and end dates
    """

    url = "https://www.newyorkfed.org/medialibrary/media/markets/Dealer_Lists_1960_to_2014.xls"
    df = pd.read_excel(url, sheet_name="Dealer Alpha", skiprows=2) 
    df = df[["Primary Dealer", "Start Date", "End Date"]]

    # ! As for now, making the end date of all dealers 2014-12-31.
    df.loc[df["End Date"] == "Current Dealer", "End Date"] = "2014-12-31"
    df["End Date"] = pd.to_datetime(df["End Date"])

    return df

def add_holding_company(df):
    """
    This function merges a manually curated mapping file (`compustat_nyfed_map_helper.csv`)
    that links primary dealers to their parent holding companies. 
    """
    # the manually edited map-heler is in the data_manual folder

    path = "./data_manual/compustat_nyfed_map_helper.csv"
    map_df = pd.read_csv(path, index_col=0)
    final_df = pd.merge(map_df, df, on="Primary Dealer", how ="left")
    return final_df



if __name__ == "__main__":
    df = pull_nyfed_dealers()
    final_df = add_holding_company(df)

    path = Path(DATA_DIR) / "primary_dealer_list.parquet"
    final_df.to_parquet(path)