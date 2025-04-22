# %% [markdown]
# # Portfolio Optimization Analysis
# Modern Portfolio Theory implementation with Efficient Frontier

# %%
import numpy as np
import matplotlib.pyplot as plt
from scripts.portfolio_optimization_core import run_optimization

# %% [markdown]
# ## Configuration
# Set portfolio assets and optimization parameters

# %%
CONFIG = {
    'assets': ["^GSPC", "EEM", "IJR"],  # SP500, MSCI EM, MSCI Small Caps
    'start_date': "2005-01-01",
    'end_date': "2025-01-01",
    'num_portfolios': 10000,
    'risk_free_rate': 0.02
}

# %% [markdown]
# ## Run Optimization
# Calculate efficient frontier and optimal portfolios

# %%
results = run_optimization(**CONFIG)
sim_results = results['simulation_results']
opt = results['optimal_portfolios']

# %% [markdown]
# ## Visualization
# Plot efficient frontier with CML bounded by portfolio risks

# %%
plt.figure(figsize=(10, 6))

# Plot random portfolios
sc = plt.scatter(sim_results[1] * 100, sim_results[0] * 100,
                c=sim_results[2], cmap='viridis', alpha=0.5,
                marker='o', s=10)

# Plot optimal portfolios
plt.scatter(opt['min_risk']['risk'] * 100, opt['min_risk']['return'] * 100,
            color='blue', s=100, marker='*',
            label='Minimum Variance Portfolio')
plt.scatter(opt['max_sharpe']['risk'] * 100, opt['max_sharpe']['return'] * 100,
            color='red', s=100, marker='*',
            label='Tangency Portfolio (Max Sharpe)')

# Calculate CML bounds based on actual portfolio risks
min_risk = np.min(sim_results[1]) * 100
max_return_idx = np.argmax(sim_results[0])
max_return_risk = sim_results[1, max_return_idx] * 100
risk_free_rate_pct = CONFIG['risk_free_rate'] * 100
max_sharpe_risk = opt['max_sharpe']['risk'] * 100
max_sharpe_return = opt['max_sharpe']['return'] * 100

# Generate CML strictly between portfolio min/max risks
cml_risks = np.linspace(min_risk, max_return_risk, 100)
cml_returns = risk_free_rate_pct + (max_sharpe_return - risk_free_rate_pct)/max_sharpe_risk * cml_risks

plt.plot(cml_risks, cml_returns, 'k--', linewidth=1.5,
         label='Capital Market Line (CML)')

# Maintain automatic axis scaling
plt.autoscale(enable=True, axis='both')

# Add plot elements
plt.colorbar(sc, label='Sharpe Ratio')
plt.title('Efficient Frontier, Tangential-Portfolio and Capital Market Line')
plt.xlabel('Volatility (Risk) [%]')
plt.ylabel('Annualized Return (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Optimal Portfolio Details
# Display allocation and performance metrics

# %%
def print_portfolio_details(name: str, details: dict, assets: list):
    print(f"\n{name}:")
    for asset, weight in zip(assets, details['weights']):
        print(f"{asset}: {weight:.2%}")
    print(f"Return: {details['return']:.2%}")
    print(f"Risk: {details['risk']:.2%}")
    print(f"Sharpe Ratio: {details['sharpe']:.2f}")

print_portfolio_details("Minimum Variance Portfolio", opt['min_risk'], CONFIG['assets'])
print_portfolio_details("\nTangency Portfolio", opt['max_sharpe'], CONFIG['assets'])