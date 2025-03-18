r"""
You can test out the latex code in the following minimal working
example document:

\documentclass{article}
\usepackage{booktabs}
\begin{document}
First document. This is a simple example, with no 
extra parameters or packages included.

\begin{table}
\centering
YOUR LATEX TABLE CODE HERE
%\input{example_table.tex}
\end{table}
\end{document}

"""
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from misc_tools import month_code_to_date
from pull_cds_return_data import *
from settings import config
from pathlib import Path
from create_portfolio import *
import datetime
DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))


## Suppress scientific notation and limit to 3 decimal places
# Sets display, but doesn't affect formatting to LaTeX
pd.set_option('display.float_format', lambda x: '%.2f' % x)
# Sets format for printing to LaTeX
float_format_func = lambda x: '{:.5f}'.format(x)

### Table 1: Replicated CDS portfolios Snapshot
df = load_portfolio()
df = pivot_table(df)[1:]
df_subset = df.iloc[:5, :10]
df_subset.index = df_subset.index.astype(int)

latex_table_string = df_subset.to_latex(float_format=float_format_func)
print(latex_table_string)

path = OUTPUT_DIR / f'latex_table1_replicated_cds.tex'
with open(path, "w") as text_file:
    text_file.write(latex_table_string)

## Table 2: Replicated CDS portfolios Summary Statistics 
# the montly return of each CDS, not portfolio
cds = load_cds_return()
cds2012 = cds[cds["trade_date"] < "2013-01-01"]
monthly_return = calc_cds_monthly_return(create_yyyymm_col(cds2012))
monthly_return_summary = monthly_return.describe()["daily_return"].to_frame()
monthly_return_summary = monthly_return_summary.rename(columns={"daily_return": "monthly_return"})[1:]

latex_table_string = monthly_return_summary .to_latex(float_format=float_format_func)


path = OUTPUT_DIR / f'latex_table2_replicated_summary.tex'
with open(path, "w") as text_file:
    text_file.write(latex_table_string)

## Graph1: ALL cds plot 
df = load_portfolio()
df = pivot_table(df).reset_index()
df["yyyymm"] = df["yyyymm"].apply(month_code_to_date)
df = df.set_index("yyyymm")

# Remove CDS_20 before plotting
if "CDS_20" in df.columns:
    df = df.drop(columns=["CDS_20"])

# Plot
plt.figure(figsize=(12, 6))
df.plot(alpha=0.7)  # Plot all CDS series with transparency

# Customize the legend to show each CDS series
plt.legend(title="CDS Portfolios", bbox_to_anchor=(1.05, 1), loc="upper left")

plt.title("CDS Portfolio Returns Over Time")
plt.xlabel("Time")
plt.ylabel("CDS Value")
plt.grid(True)

# Save the figure
plot_path = OUTPUT_DIR / "cds_portfolio_returns.png"
plt.savefig(plot_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Saved plot to: {plot_path}")




## Graph2: Pre2012: Replicated CDS portfolios vs Actual CDS portfolios
portfolio = create_portfolio.load_portfolio()
actual_cds = load_real_cds_return()

# Convert 'yyyymm' to proper date format
portfolio["yyyymm"] = portfolio["yyyymm"].apply(month_code_to_date)

# Create pivot table
portfolio_pivot = create_portfolio.pivot_table(portfolio)

# Filter the date range
portfolio_pivot = portfolio_pivot[datetime.date(2001, 1, 1) : datetime.date(2012, 12, 1)]

# Choose the column to compare
column_to_compare = "CDS_10"

# Ensure the column exists in both dataframes
if column_to_compare not in actual_cds.columns or column_to_compare not in portfolio_pivot.columns:
    print(f"Column {column_to_compare} not found in DataFrames.")
else:
    # Plot comparison
    plt.figure(figsize=(10, 5))
    plt.plot(actual_cds.index, actual_cds[column_to_compare], label="Actual", linestyle='-', marker='o')
    plt.plot(portfolio_pivot.index, portfolio_pivot[column_to_compare], label="Replication", linestyle='--', marker='x')

    plt.title(f"Comparison of {column_to_compare}: Actual vs. Replication")
    plt.xlabel("Time (yyyymm)")
    plt.ylabel("CDS Spread")
    plt.legend()
    plt.grid(True)

    # Save the figure
    comparison_plot_path = OUTPUT_DIR / f"cds_comparison_{column_to_compare}.png"
    plt.savefig(comparison_plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved comparison plot to: {comparison_plot_path}")
## Graph3: Post 2012 Graph vs Gov Bonds 
## Graph4 (Challenges): Rolling windows Correlations
