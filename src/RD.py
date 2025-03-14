import numpy as np
import pandas as pd

# Step 1: Define loss given default (LGD) 
loss_given_default = 0.6  # Assumed LGD of 60%

# Step 2: Fetch and process discount factors based on interest rates
# The function `calc_discount()` is assumed to fetch and interpolate interest rate data
quarterly_discount = calc_discount(start_date, end_date)
quarterly_discount = quarterly_discount[:-1]  # Drop the last value to align with quarter count

# Step 3: Process CDS spreads (ensuring proper filtering and formatting)
# The function `process_cds_monthly()` fetches and processes the Markit CDS spreads
cds_spread = process_cds_monthly(method=Method)

# Step 4: Filter for the required date range
cds_spread = cds_spread[(cds_spread['Date'] >= start_date) & (cds_spread['Date'] < end_date)]

# Step 5: Fill missing values by backward filling (bfill) to maintain continuity
cds_spread = cds_spread.bfill()

# Step 6: Convert 'Date' column to index for time series processing
cds_spread = cds_spread.set_index('Date')
cds_spread.index = pd.to_datetime(cds_spread.index)

# Step 7: Calculate hazard rate (lambda)
# The hazard rate λ is calculated as per the formula:
# λ = 4 * log(1 + (CDS spread / (4 * LGD)))
lambda_df = 4 * np.log(1 + (cds_spread / (4 * loss_given_default)))

# Step 8: Define the range for quarterly survival probabilities (1 to 20 quarters)
quarters = range(1, 21)  # Creating 20-quarter survival estimates

# Step 9: Initialize Risky Duration DataFrame
risky_duration = pd.DataFrame(index=lambda_df.index, columns=lambda_df.columns)

# Step 10: Loop through each CDS contract and calculate survival probabilities & risky duration
for col in lambda_df.columns:
    # Initialize DataFrame to store survival probabilities for each quarter
    quarterly_survival_probability = pd.DataFrame(index=lambda_df.index, columns=quarters)
    
    for quarter in quarters:
        # Survival probability at quarter `q`: exp(-q * λ / 4)
        quarterly_survival_probability[quarter] = np.exp(-((quarter * lambda_df[col]) / 4))
    
    # Step 11: Multiply by quarterly discount factor and sum for Risky Duration calculation
    temp_df = quarterly_survival_probability * quarterly_discount
    
    # Step 12: Compute Risky Duration as the sum of discounted survival probabilities
    risky_duration[col] = 0.25 * temp_df.sum(axis=1)  # 0.25 accounts for quarterly adjustment

# Step 13: Shift the Risky Duration by one period to get RD_t-1
risky_duration_shifted = risky_duration.shift(1)
