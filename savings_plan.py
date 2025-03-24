"""
Summary: This script simulates the investment into a savings plan over
a specific period based on historical stock data
"""

import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import utils

# Function to simulate Savings Plan investment
def simulate_savings(start_date: datetime, end_date: datetime,
                     prices: pd.Series) -> float:
    """
    Simulates the savings plan investment over a given period.

    Parameters:
    start_date (datetime): The start date of the investment period.
    end_date (datetime): The end date of the investment period.
    prices (pd.Series): A pandas Series containing the stock prices.

    Returns:
    float: The final value of the investment.
    """
    # initial investment
    initial_shares = initial_investment / prices.loc[start_date]
    total_shares = initial_shares

    # initial closing fee
    closing_fee_remaining = closing_fee_total
    # monthly dates
    monthly_dates = pd.date_range(start=start_date, end=end_date, freq='ME')
    # filter monthly dates based on saving interval
    investment_dates = monthly_dates[(saving_interval - 1)::saving_interval]
    for date in investment_dates:
        if date > end_date:
            break
        effective_rate = saving_rate - order_fee
        if closing_fee_remaining > 0:
            closing_fee = min(closing_fee_remaining,
                              saving_rate * closing_fee_rate)
            closing_fee_remaining = closing_fee_remaining - closing_fee
            effective_rate = effective_rate - closing_fee
        shares_purchased = effective_rate / prices.loc[date]
        total_shares += shares_purchased

    return total_shares * prices.loc[end_date]


# Main parameters
initial_investment = 100000  # Initial investment value
investment_period_years = 30  # Investment period in years
saving_rate = 300  # saving rate
saving_interval = 1  # saving interval in months

# Stock parameters
stock_id = '^GSPC'  # ID of the reference stock to simulate
annual_return = 0.07  # assumed annual return to scale the stock data

# Fees
order_fee = 1.50  # order fee per saving interval
annual_management_fee = 0.002  # annual management fee in percentage * 0.01

# Closing fee (just in case of an insurance-based savings plan)
closing_fee_total = 0  # closing fee
closing_fee_rate = 0.3  # share of saving rate which is used for closing fee until closing fee is reached

# Download stock data
stock_data = yf.download(stock_id, start='1970-01-01',
                         end=datetime.today().strftime('%Y-%m-%d'))
# Drop column index level with stock_id
stock_data = stock_data.droplevel(1, axis=1)

# Fill missing dates
all_dates = pd.date_range(start=stock_data.index.min(),
                          end=stock_data.index.max(), freq='D')
stock_data = stock_data.reindex(all_dates).ffill()

# Select only the adjusted close prices
stock_data = stock_data['Close']

# Scale stock data to simulate investment
stock_data = utils.scale_price_data(stock_data,
                                    1 + annual_return - annual_management_fee)

# Simulate Savings Plan
results = {
    "Start Date": [],
    "End Date": [],
    "Final Value": [],
}

end_date = stock_data.index[-1]
start_date = end_date - timedelta(days=investment_period_years * 365)

while start_date >= stock_data.index[0]:
    final_value = simulate_savings(start_date=start_date, end_date=end_date, prices=stock_data)

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

# 1st percentile (minimum amount in 99% of the cases)
percentile = np.percentile(results_df["Final Value"], 1)

# invested amount
invested_amount = saving_rate * (
            12 / saving_interval) * investment_period_years

# Plot histograms
plt.figure(figsize=(14, 7))
plt.hist(results_df["Final Value"], bins=50, alpha=0.7, color='blue',
         edgecolor='black')
plt.axvline(dca_mean, color='red', linestyle='dashed', linewidth=1,
            label='Mean')
plt.axvline(dca_median, color='orange', linestyle='dashed', linewidth=1,
            label='Median')
plt.axvline(percentile, color='purple', linestyle='dashed', linewidth=1,
            label='1st Percentile')
plt.axvline(invested_amount, color='black', linestyle='dashed', linewidth=1,
            label='Invested Amount')
plt.title('Savings Plan Results')
plt.xlabel('Portfolio Value')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()

# Print statistics
print(
    f"With a probability of 99%, the final value is higher than {percentile:.2f} €")
