import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

from pathlib import Path
from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")

from pull_markit import load_markit_data
from pull_rf_data import load_fed_yield_curve, load_fred_data


def merge_rf_data(fed_data,fred_data,markit):
    rf_data = pd.merge(fred_data,fed_data, on = "Date")
    rf_data = rf_data.merge(markit["trade_date"].drop_duplicates(),left_on="Date",right_on="trade_date", how="inner").set_index("trade_date")
    rf_data.index.name = "Date"
    return rf_data

def interpolate_row(y):
    x = [0.25,0.5,1,2,3,4,5]
    xvals = np.linspace(0.25,5,20)
    f = CubicSpline(x, y, bc_type="natural")  # Cubic spline interpolation
    return pd.Series(f(xvals), index=xvals)  # Evaluate at xvals

def calc_risk_free_rate(rf_data):
    xvals = np.linspace(0.25,5,20)
    r_t_df = pd.DataFrame(index=rf_data.index, columns=xvals)

    r_t_df.loc[:, :] = rf_data.apply(interpolate_row, axis=1)
    return r_t_df.astype(float)

def calc_lambda(cds_df, L =0.6):
    cds_df["lambda"] = 4 * np.log(1+cds_df["spread"] / 4 * L)
    return cds_df

def calc_risk_free_term(rf_data):

    r_t_df = calc_risk_free_rate(rf_data)

    maturities = np.array(r_t_df.columns, dtype= float)
    for i in range(len(r_t_df)):
        r_t_df.iloc[i] *= maturities

    r_t_df = np.exp(-1 * r_t_df / 4)
    return r_t_df


def calc_RD(cds_df, r_t_df, maturity = 5):
    cds_df["trade_date"] = pd.to_datetime(cds_df["trade_date"])

    rd_df = cds_df.merge(r_t_df, left_on = "trade_date", right_on = r_t_df.index, how = "left")
    
    rd_df = calc_lambda(rd_df)

    rd_df["RD"] = 0
    for j in range(1, 21):
    
        risk_free_col = rd_df[j/4]
        rd_df["RD"] += np.exp(-j/4*rd_df["lambda"]) * risk_free_col

    rd_df["RD"] = rd_df["RD"]/4

    return rd_df[["ticker","month","trade_date","prev_spread","spread","RD"]]



def calc_cds_daily_return(rd_df):
    # supposed previous month's cds
    rd_df["return"] = rd_df["prev_spread"] / 250 + (rd_df["spread"] - rd_df["prev_spread"]) * rd_df["RD"]
    
    return rd_df


def load_cds_return(data_dir=DATA_DIR):
    path = data_dir / "CDS_return.parquet"
    _df = pd.read_parquet(path)
    return _df

if __name__ == "__main__":
    # Load input data
    markit = load_markit_data()
    fed_data = load_fed_yield_curve()
    fred_data = load_fred_data()

    rf_data = merge_rf_data(fed_data,fred_data,markit)

    risk_free_term_df = calc_risk_free_term(rf_data)

    rd_df = calc_RD(markit, risk_free_term_df)
    final_df = calc_cds_daily_return(rd_df)

    final_df.to_parquet(DATA_DIR / "CDS_return.parquet")