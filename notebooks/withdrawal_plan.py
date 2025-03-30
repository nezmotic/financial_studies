# %% [markdown]
# # Withdrawal Plan Analysis
# Simulate portfolio withdrawals using historical market data

# %%
import matplotlib.pyplot as plt
from scripts.withdrawal_plan_core import run_withdrawal_simulation

# %% [markdown]
# ## Configuration
# Adjust withdrawal parameters and tax rules

# %%
CONFIG = {
    'initial_portfolio_value': 750000,      # Starting portfolio value
    'initial_portfolio_invested': 200000, # Initial investment value
    'monthly_withdrawal': 2500,             # Initial monthly withdrawal
    'withdrawal_period_years': 25,          # Target withdrawal duration
    'capital_gains_tax_rate': 0.1845,       # Tax rate on gains
    'tax_free_threshold': 1000,             # Annual tax-free allowance
    'selling_fee': 10,                      # Fee per withdrawal transaction
    'inflation': 0.02,                      # Annual inflation rate
    'stock_id': '^GSPC',                    # Reference index
    'annual_return': 0.07,                  # Expected annual return
    'annual_management_fee': 0.002          # Annual management fee
}

# %% [markdown]
# ## Run Simulation
# Test all possible historical starting points

# %%
results_df = run_withdrawal_simulation(CONFIG)

# %% [markdown]
# ## Results Analysis
# Visualize withdrawal success rates

# %%
# Calculate success metrics
withdrawal_target = CONFIG['withdrawal_period_years']
success_mask = results_df["Years Lasted"] >= withdrawal_target
success_rate = success_mask.mean() * 100
filtered = results_df[~success_mask]

# Create visualization
plt.figure(figsize=(12, 6))
plt.hist(filtered["Years Lasted"], bins=50, alpha=0.7, color='coral', edgecolor='black')
plt.axvline(withdrawal_target, color='black', linestyle='dashed',
           linewidth=2, label='Target Duration')
plt.title('Portfolio Longevity Distribution (below target)')
plt.xlabel('Years Sustained')
plt.ylabel('Frequency')
plt.legend()

annotation_text = f"Failure Rate: {100 - success_rate:.1f}%"
plt.gca().annotate(annotation_text, xy=(0.95, 0.95),
                  xycoords='axes fraction', ha='right',
                  fontsize=12, bbox=dict(boxstyle='round', alpha=0.1))

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Key Metrics
# Display critical performance statistics

# %%
print(f"Success Rate: {success_rate:.1f}%")
print(f"Failure Rate: {100 - success_rate:.1f}%")
print(f"Worst Case: {results_df['Years Lasted'].min():.1f} years")