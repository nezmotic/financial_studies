# Financial Studies with Python

A Python-based toolkit for simulating long-term savings plan investments, withdrawal and other strategies using historical stock market data. Analyze different investment scenarios with customizable parameters and visualize potential outcomes.

**Key Features**:
- Historical stock data integration (via Yahoo Finance)
- Customizable parameters (investment rates, stock type, fees, duration ...)
- **Exhaustive historical analysis** - simulates every possible time window in available market history
- Performance visualization with statistical metrics
- Jupyter Notebook interface for interactive analysis

### Savings Plan Simulation [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nezmotic/financial_studies/blob/main/notebooks/savings_plan.ipynb)
This analysis evaluates savings plans using historical stock data, showing the distribution of final portfolio values across all possible investment windows. Users can customize inputs like saving rate, fees, and duration, and gain insights through clear visualizations and key performance metrics.

### Withdrawal Plan Simulation [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nezmotic/financial_studies/blob/main/notebooks/withdrawal_plan.ipynb)
This analysis simulates withdrawal plans using historical stock data, showing how long a portfolio lasts across all possible starting points. It highlights the success rate, failure percentage, and distribution of failed cases, with adjustable settings for withdrawals, taxes, and fees.

### Lump Sum vs. Direct Cost Averaging [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nezmotic/financial_studies/blob/main/notebooks/lumpsum_vs_dca.ipynb)
This analysis compares lump sum investing with 12-month dollar-cost averaging (DCA) using historical stock data. Imagine a person has €100,000 to invest—should they invest it all at once or spread it over 12 months? The simulation tests all possible historical windows, showing outcome distributions and highlighting risk and performance differences through clear visualizations and key metrics.

### Portfolio Optimization Analysis [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nezmotic/financial_studies/blob/main/notebooks/portfolio_optimization.ipynb)
This analysis applies Modern Portfolio Theory to optimize asset allocation, balancing risk and return. By simulating thousands of portfolios, it identifies the Efficient Frontier and two key strategies: the lowest-risk portfolio and the optimal risk-adjusted portfolio. Visualizations map volatility versus returns, highlight the Capital Market Line, and use metrics like Sharpe ratios to compare performance, guiding data-driven allocation decisions.