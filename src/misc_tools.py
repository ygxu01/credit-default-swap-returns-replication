"""Collection of miscelaneous tools useful in a variety of situations
(not specific to the current project)
"""

import numpy as np
import pandas as pd
import polars as pl
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


from pathlib import Path
import wrds

from settings import config

DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")

from dateutil.relativedelta import relativedelta
import datetime


########################################################################################
## Pandas Helpers
########################################################################################

def generate_month_code(date):
    year = date.year
    month = date.month

    return year * 100.0 + month

def month_code_to_date(month_code):
    year = int(month_code // 100)
    month = int(month_code % 100)
    return datetime.date(year, month, 1)

def pull_from_wrds(query,wrds_username=WRDS_USERNAME):
    
    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query)
    db.close()

    return df


if __name__ == "__main__":
    pass
