"""
This module pulls and saves data on fundamentals from Compustat.
It pulls fundamentals data from Compustat needed to calculate
book equity, and the data needed from CRSP to calculate market equity.

For information about Compustat variables, see:
https://wrds-www.wharton.upenn.edu/documents/1583/Compustat_Data_Guide.pdf

"""

from pathlib import Path

import pandas as pd
import wrds
from pandas.tseries.offsets import MonthEnd

from settings import config

OUTPUT_DIR = Path(config("OUTPUT_DIR"))
DATA_DIR = Path(config("DATA_DIR"))
WRDS_USERNAME = config("WRDS_USERNAME")


def pull_compustat_with_permno(wrds_username=WRDS_USERNAME, company_name_list=[]):
    sql_in_clause = ", ".join(f"'{name}'" for name in company_name_list)
    query = f"""
    SELECT DISTINCT c.conm, c.gvkey, c.cusip, r.permno, r.permco 
    FROM comp.fundq AS c 
    LEFT JOIN crsp.msenames AS r 
    ON r.ncusip = SUBSTR(c.cusip, 1, 8) 
    WHERE c.conm IN ({sql_in_clause});"""

    db = wrds.Connection(wrds_username=wrds_username)
    comp = db.raw_sql(query, date_cols=["datadate"])
    db.close()

    return comp

