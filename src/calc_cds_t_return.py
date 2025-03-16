import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

from pull_markit import load_markit_data
from pull_rf_data import load_fed_yield_curve, load_fred_data



def interpolate_row(xvals, y):
    x = [0.25,0.5,1,2,3,4,5]
    f = CubicSpline(x, y, bc_type="natural")  # Cubic spline interpolation
    return pd.Series(f(xvals), index=xvals)  # Evaluate at xvals

def calc_risk_free_rate(rf_data):
    xvals = np.linspace(0.25,5,20)
    r_t_df = pd.DataFrame(index=rf_data.index, columns=xvals)

    r_t_df.loc[:, :] = rf_data.apply(interpolate_row, axis=1)
    return r_t_df.astype(float)

def calc_lambda(cds_df, L =0.6):
    cds_df["lambda"] = 4 * np.log(1+cds_df["midspread"] / 4 * L)
    return cds_df

def calc_risk_free_term(r_t_df):
    maturities = np.array(r_t_df.columns, dtype= float)
    for i in range(len(r_t_df)):
        r_t_df.iloc[i] *= maturities

    r_t_df = np.exp(-1 * r_t_df / 4)
    return r_t_df


def calc_RD(cds_df, r_t_df, maturity = 5):
    markit["first_trade_date"] = pd.to_datetime(markit["first_trade_date"])

    rd_df = markit.merge(r_t_df, left_on = "first_trade_date", right_on = r_t_df.index, how = "left")
    
    rd_df = calc_lambda(rd_df)

    rd_df["RD"] = 0
    for j in range(1, 21):
    
        risk_free_col = rd_df[j/4]
        rd_df["RD"] += np.exp(-j/4*rd_df["lambda"]) * risk_free_col

    rd_df["RD"] = rd_df["RD"]/4

    return rd_df[["ticker","month","first_trad_date","prev_spread","spread","RD"]]



def calc_cds_daily_return(rd_df):
    rd_df["return"] = rd_df["prev_spread"] / 250 + (rd_df["spread"] - rd_df["prev_spread"]) * rd_df["RD"]
    
    return rd_df


if __name__ == "__main__":
    markit = load_markit_data()
    fed_data = load_fed_yield_curve()
    fred_data = load_fred_data()
