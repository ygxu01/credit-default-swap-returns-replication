import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
from misc_tools import month_code_to_date
from pull_cds_return_data import *
from settings import config
from pathlib import Path
from create_portfolio import *
from pull_markit import *

import datetime

DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))

pd.set_option('display.float_format', lambda x: '%.2f' % x)
# Sets format for printing to LaTeX
float_format_func = lambda x: '{:.5f}'.format(x)

## Table1
cds_return = load_cds_return()
sector = load_sector_data()
cds_return = cds_return.merge(sector, on='ticker', how='left')
monthly_return = calc_cds_monthly_return(create_yyyymm_col(cds_return))
monthly_return = monthly_return.merge(sector, on='ticker', how='left')
sector_describe = monthly_return.groupby("sector")["daily_return"].describe()
sector_describe["count"] = sector_describe["count"].astype(int)
sector_describe = sector_describe.rename(columns={"25%": "0.25", "50%": "0.5", "75%": "0.75"})

latex_table_string = sector_describe.to_latex(float_format=float_format_func)
print(latex_table_string)

path = OUTPUT_DIR / f'latex_cds_by_sector_stats.tex'
with open(path, "w") as text_file:
    text_file.write(latex_table_string)

## Graph1
monthly_return["yyyymm"] = monthly_return["yyyymm"].apply(month_code_to_date)
monthly_grouped = monthly_return.groupby(["sector","yyyymm"])["daily_return"].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_grouped, x="yyyymm", y="daily_return", hue="sector", alpha=0.7)

plt.xlabel("Time (YYYY-MM)", fontsize=12)
plt.ylabel("Average Monthly Return", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)

# Move legend outside the plot for better visibility
plt.legend(title="Sector", bbox_to_anchor=(1.05, 1), loc='upper left')

# Save plot as PNG
output_plot_path = OUTPUT_DIR / "monthly_returns_over_time.png"
plt.savefig(output_plot_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Saved plot to: {output_plot_path}")
## Graph2
plt.figure(figsize=(12, 6))
sns.boxplot(data=monthly_grouped, x="sector", y="daily_return")

plt.xlabel("Sector", fontsize=12)
plt.ylabel("Monthly Return", fontsize=12)
plt.xticks(rotation=45)

# Save the boxplot
boxplot_path = OUTPUT_DIR / "boxplot_cds_returns_by_sector.png"
plt.savefig(boxplot_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Saved plot to: {boxplot_path}")
