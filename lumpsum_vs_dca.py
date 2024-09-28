"""Summary: This script compares the performance of a lump sum investment
 versus a Dollar-Cost Averaging (DCA) investment strategy over a specific
  period based on historical stock data"""

import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Download the stock data
stock_data = yf.download('^GSPC', start='1970-01-01', end=datetime.today().strftime('%Y-%m-%d'))

# Fill missing dates
all_dates = pd.date_range(start=stock_data.index.min(), end=stock_data.index.max(), freq='D')
stock_data = stock_data.reindex(all_dates).ffill()

# Constants
initial_investment = 100000  # Example investment amount
investment_period_years = 33
monthly_investment = initial_investment / 12

# Function to simulate lump sum investment
def simulate_lump_sum(start_date, end_date, prices):
    shares_purchased = initial_investment / prices.loc[start_date]
    final_value = shares_purchased * prices.loc[end_date]
    return final_value

# Function to simulate DCA investment
def simulate_dca(start_date, end_date, prices):
    total_shares = 0
    monthly_dates = pd.date_range(start=start_date, periods=12, freq='M')
    for date in monthly_dates:
        if date > end_date:
            break
        shares_purchased = monthly_investment / prices.loc[date]
        total_shares += shares_purchased
    final_value = total_shares * prices.loc[end_date]
    return final_value

# Simulate both strategies over all possible 10-year periods
results = {
    "Start Date": [],
    "End Date": [],
    "Lump Sum Value": [],
    "DCA Value": []
}

end_date = stock_data.index[-1]
start_date = end_date - timedelta(days=investment_period_years * 365)

while start_date >= stock_data.index[0]:
    lump_sum_value = simulate_lump_sum(start_date, end_date, stock_data['Adj Close'])
    dca_value = simulate_dca(start_date, end_date, stock_data['Adj Close'])

    results["Start Date"].append(start_date)
    results["End Date"].append(end_date)
    results["Lump Sum Value"].append(lump_sum_value)
    results["DCA Value"].append(dca_value)

    start_date -= timedelta(days=1)
    end_date -= timedelta(days=1)

# Create a DataFrame for better visualization
results_df = pd.DataFrame(results)
print(results_df)

# Calculate statistics
lump_sum_mean = results_df["Lump Sum Value"].mean()
dca_mean = results_df["DCA Value"].mean()
lump_sum_median = results_df["Lump Sum Value"].median()
dca_median = results_df["DCA Value"].median()
lump_sum_std = results_df["Lump Sum Value"].std()
dca_std = results_df["DCA Value"].std()

# 90% confidence interval
lump_sum_ci = 1.645 * lump_sum_std
dca_ci = 1.645 * dca_std

# 5th percentile (minimum amount in 95% of the cases)
lump_sum_5th_percentile = np.percentile(results_df["Lump Sum Value"], 5)
dca_5th_percentile = np.percentile(results_df["DCA Value"], 5)

# Plot histograms
plt.figure(figsize=(14, 7))

# Lump Sum
plt.subplot(1, 2, 1)
plt.hist(results_df["Lump Sum Value"], bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(lump_sum_mean, color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(lump_sum_median, color='orange', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(lump_sum_mean + lump_sum_ci, color='green', linestyle='dashed', linewidth=1, label='90% CI')
plt.axvline(lump_sum_mean - lump_sum_ci, color='green', linestyle='dashed', linewidth=1)
plt.axvline(lump_sum_5th_percentile, color='purple', linestyle='dashed', linewidth=1, label='5th Percentile')
plt.title('Lump Sum Investment')
plt.xlabel('Portfolio Value')
plt.ylabel('Frequency')
plt.legend()

# DCA
plt.subplot(1, 2, 2)
plt.hist(results_df["DCA Value"], bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(dca_mean, color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(dca_median, color='orange', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(dca_mean + dca_ci, color='green', linestyle='dashed', linewidth=1, label='90% CI')
plt.axvline(dca_mean - dca_ci, color='green', linestyle='dashed', linewidth=1)
plt.axvline(dca_5th_percentile, color='purple', linestyle='dashed', linewidth=1, label='5th Percentile')
plt.title('Dollar-Cost Averaging (DCA) Investment')
plt.xlabel('Portfolio Value')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()