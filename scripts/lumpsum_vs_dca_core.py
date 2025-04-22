"""Core functionality for comparing Lump Sum vs DCA"""
from datetime import datetime
import pandas as pd
from typing import Dict
from scripts.utils import download_stock_data, scale_price_data


def simulate_lump_sum(prices: pd.Series, start_date: datetime,
                      end_date: datetime, config: Dict) -> float:
    """Simulate lump sum investment strategy"""
    shares = config['initial_investment'] / prices.loc[start_date]
    return shares * prices.loc[end_date]


def simulate_dca(prices: pd.Series, start_date: datetime,
                 end_date: datetime, config: Dict) -> float:
    """Simulate 12-month Dollar-Cost Averaging strategy"""
    monthly_dates = pd.date_range(start=start_date, periods=12, freq='ME')
    total_shares = 0

    for date in monthly_dates:
        if date > end_date or date not in prices.index:
            continue
        shares = config['monthly_investment'] / prices.loc[date]
        total_shares += shares

    return total_shares * prices.loc[end_date]


def run_simulation(config: Dict) -> pd.DataFrame:
    """Run simulation across all historical periods"""
    raw_data = download_stock_data(config['stock_id'])
    scaled_prices = scale_price_data(raw_data, 1 + config['annual_return'])

    investment_days = config['investment_period_years'] * 365
    windows = pd.DataFrame({
        'Start Date': scaled_prices.index[:-investment_days],
        'End Date': scaled_prices.index[investment_days:]
    })

    windows['Lump Sum'] = windows.apply(
        lambda row: simulate_lump_sum(scaled_prices, row['Start Date'],
                                      row['End Date'], config), axis=1)

    windows['DCA'] = windows.apply(
        lambda row: simulate_dca(scaled_prices, row['Start Date'],
                                 row['End Date'], config), axis=1)

    return windows.dropna()