"""
Collection of miscellaneous tools useful in a variety of situations
(not specific to the current project).
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

from pathlib import Path
import wrds
import datetime
from settings import config

# Load project-specific configurations
DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")
START_YEAR = config("START_YEAR")
END_YEAR = config("END_YEAR")


########################################################################################
## Date and Time Utilities
########################################################################################


def generate_month_code(date):
    """
    Convert a date into a numeric month code (YYYYMM).

    Example:
    >>> generate_month_code(datetime.date(2024, 5, 1))
    202405
    """
    return date.year * 100.0 + date.month


def month_code_to_date(month_code):
    """
    Convert a numeric month code (YYYYMM) to a datetime.date.

    Example:
    >>> month_code_to_date(202405)
    datetime.date(2024, 5, 1)
    """
    return datetime.date(int(month_code // 100), int(month_code % 100), 1)


########################################################################################
## WRDS Data Retrieval
########################################################################################


def pull_from_wrds(query, wrds_username=WRDS_USERNAME):
    """
    Retrieve data from WRDS using a SQL query.

    Example:
    >>> df = pull_from_wrds("SELECT * FROM my_table LIMIT 10")
    >>> isinstance(df, pd.DataFrame)
    True
    """
    db = wrds.Connection(wrds_username=wrds_username)
    df = db.raw_sql(query)
    db.close()
    return df


if __name__ == "__main__":
    pass
