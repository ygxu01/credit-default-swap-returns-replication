actual_df.plot(figsize=(12, 6), title="CDS Time Series")

plt.xlabel("Time (yyyymm)")
plt.ylabel("Values")
plt.legend(title="CDS Series")
plt.grid(True)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

actual_df.plot(figsize=(12, 6), title="CDS Time Series")

plt.xlabel("Time (yyyymm)")
plt.ylabel("Values")
plt.legend(title="CDS Series")
plt.grid(True)
plt.show()



def plot_cds_comparison(df_actual, df_replication, column_name):
    """
    Plots the comparison of actual vs. replicated values for a given CDS column.

    Parameters:
    df_actual (DataFrame): DataFrame containing actual CDS values.
    df_replication (DataFrame): DataFrame containing replicated CDS values.
    column_name (str): The column name (CDS series) to plot.
    """
    if column_name not in df_actual.columns or column_name not in df_replication.columns:
        print(f"Column {column_name} not found in DataFrames.")
        return
    
    plt.figure(figsize=(10, 5))
    plt.plot(df_actual.index, df_actual[column_name], label="Actual", linestyle='-', marker='o')
    plt.plot(df_replication.index, df_replication[column_name], label="Replication", linestyle='--', marker='x')
    
    plt.title(f"Comparison of {column_name}: Actual vs. Replication")
    plt.xlabel("Time (yyyymm)")
    plt.ylabel("CDS Spread")
    plt.legend()
    plt.grid(True)
    plt.show()