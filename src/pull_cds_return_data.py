import pandas as pd
from pandas.tseries.offsets import MonthEnd
from pathlib import Path
from settings import config
from misc_tools import month_code_to_date

MANUAL_DATA_DIR = Path(config("MANUAL_DATA_DIR"))
DATA_DIR = Path(config("DATA_DIR"))

def pull_real_cds_return():
    '''
    Reading the original returns which were to be replicated
    '''
    path = MANUAL_DATA_DIR / "He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv"
    actual_return = pd.read_csv(path)
    actual_return = actual_return[['yyyymm','CDS_01','CDS_02','CDS_03','CDS_04','CDS_05','CDS_06','CDS_07','CDS_08','CDS_09','CDS_10','CDS_11','CDS_12','CDS_13','CDS_14','CDS_15','CDS_16','CDS_17','CDS_18','CDS_19','CDS_20']]
    actual_return["yyyymm"] = actual_return["yyyymm"].apply(month_code_to_date)
    actual_return = actual_return.set_index("yyyymm")
    actual_return = actual_return.dropna(axis=0)
    return actual_return


def unpivot_table(real_cds_return):
    '''
    Unpivoting the table to get the returns in long format
    '''

    df_unpivoted = real_cds_return.reset_index().melt(id_vars=['yyyymm'], var_name='portfolio', value_name='monthly_return')

    df_unpivoted['portfolio'] = df_unpivoted['portfolio'].str.extract(r'(\d+)').astype(int)

    return df_unpivoted


def load_real_cds_return(data_dir = DATA_DIR):
    path = data_dir / "actual_cds_return.parquet"
    _df = pd.read_parquet(path)
    return _df

if __name__ == "__main__":
    df = pull_real_cds_return()
    df.to_parquet(DATA_DIR / "actual_cds_return.parquet")
