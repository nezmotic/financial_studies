"""Summary: This script simulates the withdrawal of a fixed amount of money
from a portfolio invested in the S&P 500 index over a specific period"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Constants
initial_portfolio_value = 700000  # Example initial portfolio value
monthly_withdrawal = 2573  # Example monthly withdrawal amount
capital_gains_tax_rate = 0.1845  # Capital gains tax rate
withdrawal_period_years = 25 # Withdrawal period in years
stock_id = '^GSPC' # ID of the stock to simulate

# Download stock data
stock_data = yf.download(stock_id, start='1970-01-01', end=datetime.today().strftime('%Y-%m-%d'))

# Fill missing dates
all_dates = pd.date_range(start=stock_data.index.min(), end=stock_data.index.max(), freq='D')
stock_data = stock_data.reindex(all_dates).ffill()

# Function to simulate withdrawals
def simulate_withdrawals(start_date, end_date, prices):
    portfolio_value = initial_portfolio_value
    current_date = start_date
    years_last = 0

    while portfolio_value > 0 and current_date < end_date:
        # Calculate monthly return
        if current_date + timedelta(days=30) < prices.index[-1]:
            next_date = current_date + timedelta(days=30)
        else:
            next_date = end_date

        monthly_return = (prices.loc[next_date] / prices.loc[current_date]) - 1

        # Withdraw amount
        withdrawal_amount = monthly_withdrawal
        # Calculate capital gains tax
        capital_gains = withdrawal_amount * capital_gains_tax_rate
        total_withdrawal = withdrawal_amount + capital_gains
        # Update portfolio value
        portfolio_value = (portfolio_value - total_withdrawal) * (1 + monthly_return)
        # Move to next month
        current_date = next_date
        years_last += 1 / 12

    return years_last


# Simulate withdrawals over all possible start dates
results = {
    "Start Date": [],
    "Years Lasted": []
}

end_date = stock_data.index[-1] - timedelta(days=withdrawal_period_years * 365)
start_date = stock_data.index[0]

while start_date <= end_date:
    years_lasted = simulate_withdrawals(start_date, start_date + timedelta(days=withdrawal_period_years * 365), stock_data['Adj Close'])
    results["Start Date"].append(start_date)
    results["Years Lasted"].append(years_lasted)
    start_date += timedelta(days=1)

# Create a DataFrame for better visualization
results_df = pd.DataFrame(results)

# Filter results below withdrawal_period_years
filtered_results_df = results_df[results_df["Years Lasted"] < withdrawal_period_years]

# Calculate the percentage of simulations below withdrawal_period_years
percentage_below_withdrawal_period = (filtered_results_df.shape[0] / results_df.shape[0]) * 100

# Plot histogram of years lasted
plt.figure(figsize=(10, 6))
plt.hist(filtered_results_df["Years Lasted"], bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(withdrawal_period_years, color='purple', linestyle='dashed', linewidth=1, label='withdrawel period')
plt.title('Distribution of Years Portfolio Lasted')
plt.xlabel('Years')
plt.ylabel('Frequency')
plt.legend()
plt.text(0.95, 0.95, f'{percentage_below_withdrawal_period:.2f}% of simulations below withdrawel period',
         horizontalalignment='right', verticalalignment='top', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
plt.show()
