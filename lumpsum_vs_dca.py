"""
Summary: This script compares the performance of a lump sum investment
versus a Dollar-Cost Averaging (DCA) investment strategy over a specific
period based on historical stock data
"""

import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import utils


def simulate_lump_sum(start_date: datetime, end_date: datetime, prices: pd.Series) -> float:
    """
    Simulates a lump sum investment over a given period.

    Parameters:
    start_date (datetime): The start date of the investment period.
    end_date (datetime): The end date of the investment period.
    prices (pd.Series): A pandas Series containing the stock prices.

    Returns:
    float: The final value of the investment.
    """
    shares_purchased = initial_investment / prices.loc[start_date]
    final_value = shares_purchased * prices.loc[end_date]
    return final_value.iloc[0]


def simulate_dca(start_date: datetime, end_date: datetime, prices: pd.Series) -> float:
    """
    Simulates a Dollar-Cost Averaging (DCA) investment over a given period.

    Parameters:
    start_date (datetime): The start date of the investment period.
    end_date (datetime): The end date of the investment period.
    prices (pd.Series): A pandas Series containing the stock prices.

    Returns:
    float: The final value of the investment.
    """
    total_shares = 0
    monthly_dates = pd.date_range(start=start_date, periods=12, freq='ME')
    for date in monthly_dates:
        if date > end_date:
            break
        shares_purchased = monthly_investment / prices.loc[date]
        total_shares += shares_purchased
    final_value = total_shares * prices.loc[end_date]
    return final_value.iloc[0]


# Main parameters
initial_investment = 100000
investment_period_years = 30
monthly_investment = initial_investment / 12

# Stock parameters
stock_id = '^GSPC' # ID of the stock to simulate
annual_return = 0.07  # assumed annual return to scale the stock data

# Download the stock data
stock_data = yf.download(stock_id, start='1970-01-01', end=datetime.today().strftime('%Y-%m-%d'))

# Fill missing dates
all_dates = pd.date_range(start=stock_data.index.min(), end=stock_data.index.max(), freq='D')
stock_data = stock_data.reindex(all_dates).ffill()

# Select only the adjusted close prices
stock_data = stock_data['Close'].dropna()

# Scale stock data to simulate investment
stock_data = utils.scale_price_data(stock_data, 1 + annual_return)

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
    lump_sum_value = simulate_lump_sum(start_date=start_date, end_date=end_date, prices=stock_data)
    dca_value = simulate_dca(start_date=start_date, end_date=end_date, prices=stock_data)

    results["Start Date"].append(start_date)
    results["End Date"].append(end_date)
    results["Lump Sum Value"].append(lump_sum_value)
    results["DCA Value"].append(dca_value)

    start_date -= timedelta(days=1)
    end_date -= timedelta(days=1)

# Create a DataFrame for better visualization, but ignore column names
results_df = pd.DataFrame(results)

# Calculate statistics
lump_sum_mean = results_df["Lump Sum Value"].mean()
dca_mean = results_df["DCA Value"].mean()
lump_sum_median = results_df["Lump Sum Value"].median()
dca_median = results_df["DCA Value"].median()

# 5th percentile (minimum amount in 95% of the cases)
lump_sum_percentile = np.percentile(results_df["Lump Sum Value"], 1)
dca_percentile = np.percentile(results_df["DCA Value"], 1)

# Plot histograms
plt.figure(figsize=(14, 7))

# Lump Sum
plt.subplot(1, 2, 1)
plt.hist(results_df["Lump Sum Value"], bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(lump_sum_mean, color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(lump_sum_median, color='orange', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(lump_sum_percentile, color='purple', linestyle='dashed', linewidth=1, label='1st Percentile')
plt.title('Lump Sum Investment')
plt.xlabel('Portfolio Value')
plt.ylabel('Frequency')
plt.legend()

# DCA
plt.subplot(1, 2, 2)
plt.hist(results_df["DCA Value"], bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(dca_mean, color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(dca_median, color='orange', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(dca_percentile, color='purple', linestyle='dashed', linewidth=1, label='1st Percentile')
plt.title('Dollar-Cost Averaging (DCA) Investment')
plt.xlabel('Portfolio Value')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()

# Print statistics
print(
    f"Lump Sum: With a probability of 99%, the final value is higher than {lump_sum_percentile:.2f} €")

print(
    f"DCA: With a probability of 99%, the final value is higher than {dca_percentile:.2f} €")
