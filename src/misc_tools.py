"""Collection of miscelaneous tools useful in a variety of situations
(not specific to the current project)
"""

import numpy as np
import pandas as pd
import polars as pl
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

from dateutil.relativedelta import relativedelta
import datetime


########################################################################################
## Pandas Helpers
########################################################################################

def generate_month_code(date):
    year = date.year
    month = date.month

    return year * 100.0 + month


if __name__ == "__main__":
    pass
