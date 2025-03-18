"""
This file evaluates the replication results by comparing key trends with the 
original paper.

Since the paper does not fully specify the data sources, variable definitions, 
or exact methodology, a perfect match is not feasible. Additionally, the paper 
groups CDS into 20 portfolios, which can amplify small deviations.

To assess replication accuracy, we focus on correlation analysis between the 
original and replicated values, ensuring that the overall trends align with the 
expected results.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from settings import config
from create_portfolio import load_portfolio, pivot_table
from pull_cds_return_data import load_real_cds_return
from misc_tools import month_code_to_date


DATA_DIR = Path(config("DATA_DIR"))

def test_cds_correlation():
    """
    Test that the replicated CDS portfolio returns have a reasonable correlation with actual CDS returns.
    """
    he_table = load_real_cds_return()
    portfolio = load_portfolio()

    portfolio_pivot = pivot_table(portfolio)
    portfolio_pivot = portfolio_pivot.reset_index()
    portfolio_pivot["yyyymm"] = portfolio_pivot["yyyymm"].apply(month_code_to_date)
    portfolio_pivot = portfolio_pivot.set_index("yyyymm")

    # portfolio file includes 200101 data, but he_table starts from 200102
    portfolio_pivot = portfolio_pivot[1:61]
    he_table = he_table.iloc[0:60]

    avg_replication = portfolio_pivot.mean(axis=1) 
    avg_original = he_table.mean(axis=1)

    correlation_avg = avg_replication.corr(avg_original)

    # Check if correlation is sufficiently high
    assert correlation_avg > 0.75, f"Correlation too low: {correlation_avg}"

