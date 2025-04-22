"""
Summary:Useful utility functions for the project
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime


def calculate_tax(
                withdrawal_amount: float,
                tax_rate: float,
                tax_free_threshold: float = 0,
                cost_basis: float = 0
) -> float:
    """
    Calculate capital gains tax on withdrawal amount considering:
    - Tax-free threshold (monthly)
    - Cost basis (portion not subject to tax)
    """
    taxable_amount = max(
        (withdrawal_amount - tax_free_threshold) - cost_basis,
        0
    )
    return taxable_amount * tax_rate


def download_stock_data(stock_id: str) -> pd.Series:
    """Download and process historical stock data"""
    stock_data = yf.download(stock_id, start='1970-01-01',
                             end=datetime.today().strftime('%Y-%m-%d'))
    stock_data = stock_data.droplevel(1,
                                      axis=1) if stock_data.columns.nlevels > 1 else stock_data
    all_dates = pd.date_range(start=stock_data.index.min(),
                              end=stock_data.index.max(), freq='D')
    return stock_data.reindex(all_dates).ffill()['Close']


def scale_price_data(price_data: pd.Series,
                     target_interest_rate: float) -> pd.Series:
    """
    Scales the given price data to match the target interest rate.

    Parameters:
    price_data (pd.Series): A pandas Series containing the price data to be scaled.
    target_interest_rate (float): The target interest rate to scale the price data to.

    Returns:
    pd.Series: A pandas Series containing the scaled price data.
    """
    price_ratio = price_data.iloc[-1] / price_data.iloc[0]
    years = (price_data.index[-1] - price_data.index[0]).days / 365
    interest_rate = price_ratio ** (1 / years)
    price_data_scaled = price_data.copy()
    for i in range(len(price_data)):
        price_data_scaled.iloc[i] = price_data.iloc[i] * (
                target_interest_rate / interest_rate) ** (
                                            i * years / len(price_data))
    return price_data_scaled


if __name__ == "__main__":
    dummy_data = pd.Series(np.linspace(100, 110, 366).tolist(),
                           index=pd.date_range(start='1/1/2001', periods=366,
                                               freq='D'))
    dummy_data = scale_price_data(dummy_data, 1.20)
    print(dummy_data)
