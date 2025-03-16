import pandas as pd
from pandas.tseries.offsets import MonthEnd
from pathlib import Path
from settings import config

MANUAL_DATA_DIR = Path(config("MANUAL_DATA_DIR"))
DATA_DIR = Path(config("DATA_DIR"))

def pull_real_cds_return():
    '''
    Reading the original returns which were to be replicated
    '''
    path = MANUAL_DATA_DIR / "He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv"
    actual_return = pd.read_csv(path)
    actual_return = actual_return[['yyyymm','CDS_01','CDS_02','CDS_03','CDS_04','CDS_05','CDS_06','CDS_07','CDS_08','CDS_09','CDS_10','CDS_11','CDS_12','CDS_13','CDS_14','CDS_15','CDS_16','CDS_17','CDS_18','CDS_19','CDS_20']]
    actual_return = actual_return.dropna(axis=0)
    return actual_return

if __name__ == "__main__":
    df = pull_real_cds_return()
    df.to_parquet(DATA_DIR / "actual_cds_return.parquet")