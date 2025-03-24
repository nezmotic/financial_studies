"""
Summary: Portfolio optimization using the Efficient Frontier and the Capital Market Line (CML).
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def portfolio_performance(weights, mean_returns, cov_matrix):
    """
    Calculates the performance metrics of a portfolio.

    Parameters:
    weights (numpy.ndarray): Array of asset weights in the portfolio.
    mean_returns (pandas.Series): Series of mean returns for each asset.
    cov_matrix (pandas.DataFrame): Covariance matrix of asset returns.

    Returns:
    tuple: A tuple containing:
        - portfolio_return (float): The expected return of the portfolio.
        - portfolio_risk (float): The standard deviation (risk) of the portfolio.
        - sharpe_ratio (float): The Sharpe ratio of the portfolio.
    """
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = portfolio_return / portfolio_risk
    return portfolio_return, portfolio_risk, sharpe_ratio

# Main parameters
assets = ["BREB.BR", "AGT.L", "BRK-B", "INVE-A.ST"]
#assets = ["^GSPC", "EEM", "IJR"]  # SP500, MSCI EM, MSCI Small Caps
#assets = ["^GSPC", "EEM"]  # SP500, MSCI EM
#assets = ["CGT.L", "BREB.BR"]

start_date = "2000-01-01"
end_date = "2024-01-01"
num_portfolios = 10000

# Download historical data
prices = yf.download(assets, start=start_date, end=end_date)["Close"].dropna()

# Calculate logarithmic returns
returns = np.log(prices / prices.shift(1)).dropna()

# Calculate mean returns and covariance matrix
mean_returns = returns.mean()
cov_matrix = returns.cov()
num_assets = len(assets)

# Generate random portfolios
results = np.zeros((3, num_portfolios))
weights_list = []

for i in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    weights_list.append(weights)
    portfolio_return, portfolio_risk, sharpe_ratio = portfolio_performance(weights, mean_returns, cov_matrix)
    results[0, i] = portfolio_return
    results[1, i] = portfolio_risk
    results[2, i] = sharpe_ratio

# Find portfolio with maximum Sharpe Ratio
max_sharpe_idx = np.argmax(results[2])
max_sharpe_weights = weights_list[max_sharpe_idx]
max_sharpe_return, max_sharpe_risk, max_sharpe_ratio = portfolio_performance(max_sharpe_weights, mean_returns, cov_matrix)

# Find portfolio with minimum risk
min_risk_idx = np.argmin(results[1])
min_risk_weights = weights_list[min_risk_idx]
min_risk_return, min_risk_risk, _ = portfolio_performance(min_risk_weights, mean_returns, cov_matrix)

# Plot efficiency curve
plt.figure(figsize=(10, 6))
plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap="viridis", marker="o", s=10, alpha=0.5)
plt.colorbar(label="Sharpe Ratio")
plt.scatter(min_risk_risk, min_risk_return, color="red", label="Minimum-Variance Portfolio", zorder=5)
plt.scatter(max_sharpe_risk, max_sharpe_return, color="blue", label="Tangency Portfolio (Max Sharpe)", zorder=5)

# Annotate portfolios
plt.annotate(
    f"MVP\nRisk: {min_risk_risk:.2%}\nReturn: {min_risk_return:.2%}",
    (min_risk_risk, min_risk_return),
    textcoords="offset points",
    xytext=(-70, -30),
    ha="center",
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color="red")
)
plt.annotate(
    f"Max Sharpe\nRisk: {max_sharpe_risk:.2%}\nReturn: {max_sharpe_return:.2%}\nSharpe: {max_sharpe_ratio:.2f}",
    (max_sharpe_risk, max_sharpe_return),
    textcoords="offset points",
    xytext=(50, 20),
    ha="center",
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color="blue")
)

# Add plot details
plt.title("Efficient Frontier with Tangency Portfolio and Minimum-Variance Portfolio")
plt.xlabel("Portfolio Risk (Standard Deviation)")
plt.ylabel("Portfolio Return")
plt.legend()
plt.grid(True)
plt.show()

# Print portfolio details
print("Minimum-Variance Portfolio:")
for asset, weight in zip(assets, min_risk_weights):
    print(f"{asset}: {weight:.2%}")
print(f"Return: {min_risk_return:.2%}, Risk: {min_risk_risk:.2%}")

print("\nTangency Portfolio (Maximum Sharpe Ratio):")
for asset, weight in zip(assets, max_sharpe_weights):
    print(f"{asset}: {weight:.2%}")
print(f"Return: {max_sharpe_return:.2%}, Risk: {max_sharpe_risk:.2%}, Sharpe Ratio: {max_sharpe_ratio:.2f}")
