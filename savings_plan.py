"""Summary: This script simulates the investment into a savings plan over
 a specific period based on historical stock data"""

import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Input parameters
initial_investment = 0  # Initial investment value
investment_period_years = 30 # Investment period in years
saving_rate = 1200 # saving rate
saving_interval = 12 # saving interval in months
order_fee = 1.50 # order fee
stock_id = '^GSPC'

# Download stock data
stock_data = yf.download(stock_id, start='1970-01-01', end=datetime.today().strftime('%Y-%m-%d'))

# Fill missing dates
all_dates = pd.date_range(start=stock_data.index.min(), end=stock_data.index.max(), freq='D')
stock_data = stock_data.reindex(all_dates).ffill()

# Function to simulate Savings Plan investment
def simulate_savings(start_date, end_date, prices):
    # Initial investment
    initial_shares = initial_investment / prices.loc[start_date]
    total_shares = initial_shares

    # investments
    monthly_dates = pd.date_range(start=start_date, end=end_date, freq='M')
    # filter dates based on saving interval
    investment_dates = monthly_dates[(saving_interval-1)::saving_interval]
    for date in investment_dates:
        if date > end_date:
            break
        shares_purchased = (saving_rate-order_fee) / prices.loc[date]
        total_shares += shares_purchased

    final_value = total_shares * prices.loc[end_date]
    return final_value

# Simulate Savings Plan
results = {
    "Start Date": [],
    "End Date": [],
    "Final Value": [],
}

end_date = stock_data.index[-1]
start_date = end_date - timedelta(days=investment_period_years * 365)

while start_date >= stock_data.index[0]:
    final_value = simulate_savings(start_date, end_date, stock_data['Adj Close'])

    results["Start Date"].append(start_date)
    results["End Date"].append(end_date)
    results["Final Value"].append(final_value)

    start_date -= timedelta(days=1)
    end_date -= timedelta(days=1)

# Create a DataFrame for better visualization
results_df = pd.DataFrame(results)

# Calculate statistics
dca_mean = results_df["Final Value"].mean()
dca_median = results_df["Final Value"].median()
dca_std = results_df["Final Value"].std()

# 90% confidence interval
dca_ci = 1.645 * dca_std

# 5th percentile (minimum amount in 95% of the cases)
dca_5th_percentile = np.percentile(results_df["Final Value"], 5)

# invested amount
invested_amount = saving_rate * (12/saving_interval) * investment_period_years

# Plot histograms
plt.figure(figsize=(14, 7))
plt.hist(results_df["Final Value"], bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(dca_mean, color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(dca_median, color='orange', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(dca_mean + dca_ci, color='green', linestyle='dashed', linewidth=1, label='90% CI')
plt.axvline(dca_mean - dca_ci, color='green', linestyle='dashed', linewidth=1)
plt.axvline(dca_5th_percentile, color='purple', linestyle='dashed', linewidth=1, label='5th Percentile')
plt.axvline(invested_amount, color='black', linestyle='dashed', linewidth=1, label='Invested Amount')
plt.title('Savings Plan Results')
plt.xlabel('Portfolio Value')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()