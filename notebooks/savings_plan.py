# %% [markdown]
# # Savings Plan Analysis
# This script simulates the investment into a savings plan over
# a specific period based on historical stock data

# %%
import matplotlib.pyplot as plt
import numpy as np
from scripts.savings_plan_core import run_simulation

# %% [markdown]
# ## Configuration
# Adjust these parameters to run different saving plan scenarios

# %%
CONFIG = {
    'initial_investment': 100000,    # Initial investment in €
    'investment_period_years': 30,   # Investment duration
    'saving_rate': 300,              # Monthly saving amount
    'saving_interval': 1,            # Months between savings
    'stock_id': '^GSPC',             # Stock index to track
    'annual_return': 0.07,           # Expected annual return
    'order_fee': 1.50,               # Fee per transaction
    'annual_management_fee': 0.002,  # Annual management fee
    'closing_fee_total': 0,          # Total closing fees
    'closing_fee_rate': 0.3          # Closing fee rate
}

# %% [markdown]
# ## Run Simulation
# Simulate the savings plan for all possible investment windows

# %%
results_df = run_simulation(CONFIG)

# %% [markdown]
# ## Analysis & Visualization
# Analyze the distribution of the final portfolio values

# %%
# Calculate statistics
mean = results_df["Final Value"].mean()
median = results_df["Final Value"].median()
percentile = np.percentile(results_df["Final Value"], 1)
invested = CONFIG['saving_rate'] * (12 / CONFIG['saving_interval']) * CONFIG['investment_period_years']

# Create visualization
plt.figure(figsize=(12, 6))
plt.hist(results_df["Final Value"], bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(mean, color='red', linestyle='dashed', linewidth=1, label='Mean')
plt.axvline(median, color='orange', linestyle='dashed', linewidth=1, label='Median')
plt.axvline(percentile, color='purple', linestyle='dashed', linewidth=1, label='1st Percentile')
plt.axvline(invested, color='black', linestyle='dashed', linewidth=2, label='Invested Amount')

plt.title('Savings Plan Performance Distribution')
plt.xlabel('Portfolio Value (€)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Key Metrics
# Display the key metrics of the savings plan distribution

# %%
print(f"Average Final Value: €{mean:,.2f}")
print(f"Median Final Value: €{median:,.2f}")
print(f"1st Percentile Value: €{percentile:,.2f}")
print(f"Total Invested Amount: €{invested:,.2f}")