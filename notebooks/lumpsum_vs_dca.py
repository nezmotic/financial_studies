# %% [markdown]
# # Lump Sum vs DCA Comparison
# Compare investment strategies using historical market data

# %%
import matplotlib.pyplot as plt
import numpy as np
from scripts.lumpsum_vs_dca_core import run_comparison_simulation

# %% [markdown]
# ## Configuration
# Set investment parameters and strategy settings

# %%
CONFIG = {
    'initial_investment': 100000,       # Total investment amount
    'investment_period_years': 30,      # Investment duration
    'monthly_investment': 100000/12,    # DCA monthly amount
    'stock_id': '^GSPC',                # Reference index
    'annual_return': 0.07               # Expected annual return
}

# %% [markdown]
# ## Run Simulation
# Execute comparison across all historical windows

# %%
results_df = run_comparison_simulation(CONFIG)

# %% [markdown]
# ## Strategy Analysis
# Visualize performance distributions

# %%
# Calculate statistics
metrics = {
    'Lump Sum Mean': results_df['Lump Sum'].mean(),
    'DCA Mean': results_df['DCA'].mean(),
    'Lump Sum Median': results_df['Lump Sum'].median(),
    'DCA Median': results_df['DCA'].median(),
    'Lump Sum 1st %': np.percentile(results_df['Lump Sum'], 1),
    'DCA 1st %': np.percentile(results_df['DCA'], 1)
}

# Create visualization
plt.figure(figsize=(14, 6))

# Lump Sum distribution
plt.subplot(1, 2, 1)
plt.hist(results_df['Lump Sum'], bins=50, alpha=0.7, color='navy', edgecolor='black')
plt.axvline(metrics['Lump Sum Mean'], color='red', linestyle='--', label='Mean')
plt.axvline(metrics['Lump Sum Median'], color='orange', linestyle='--', label='Median')
plt.axvline(metrics['Lump Sum 1st %'], color='purple', linestyle='dashed', linewidth=1, label='1st Percentile')
plt.title('Lump Sum Performance')
plt.xlabel('Portfolio Value (€)')
plt.ylabel('Frequency')
plt.legend()

# DCA distribution
plt.subplot(1, 2, 2)
plt.hist(results_df['DCA'], bins=50, alpha=0.7, color='green', edgecolor='black')
plt.axvline(metrics['DCA Mean'], color='red', linestyle='--', label='Mean')
plt.axvline(metrics['DCA Median'], color='orange', linestyle='--', label='Median')
plt.axvline(metrics['DCA 1st %'], color='purple', linestyle='dashed', linewidth=1, label='1st Percentile')
plt.title('DCA Performance')
plt.xlabel('Portfolio Value (€)')
plt.legend()

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Comparative Metrics
# Display key performance indicators

# %%
print(f"Lump Sum: Average Final Value: €{metrics['Lump Sum Mean']:,.2f}")
print(f"Lump Sum: Median Final Value: €{metrics['Lump Sum Median']:,.2f}")
print(f"Lump Sum: 1st Percentile Value: €{metrics['Lump Sum 1st %']:,.2f}")

print(f"DCA: Average Final Value: €{metrics['DCA Mean']:,.2f}")
print(f"DCA: Median Final Value: €{metrics['DCA Median']:,.2f}")
print(f"DCA: 1st Percentile Value: €{metrics['DCA 1st %']:,.2f}")



