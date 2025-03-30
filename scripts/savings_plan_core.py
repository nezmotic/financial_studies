"""Core functionality for savings plan simulations"""

import pandas as pd
import numpy as np
from typing import Dict
from scripts.utils import scale_price_data, download_stock_data


def precalculate_investment_dates(start, end, interval):
    """Pre-calculate all possible investment dates upfront"""
    dates = pd.date_range(start=start, end=end, freq=f'{interval}MS')
    return dates[(dates >= start) & (dates <= end)]


# Optimized simulate_savings
def simulate_savings(prices, start_date, end_date, config):
    """Simulate the savings plan for a specific period based on historical
    stock data"""
    iv_dates = precalculate_investment_dates(start_date, end_date,
                                             config['saving_interval'])

    if not iv_dates.empty:
        effective_rates = calculate_effective_rates(config, len(iv_dates))
        shares = effective_rates / prices.loc[iv_dates].values
        total_shares = shares.sum()
    else:
        total_shares = 0

    initial_shares = config['initial_investment'] / prices.loc[start_date]
    return (total_shares + initial_shares) * prices.loc[end_date]


def calculate_effective_rates(config, num_periods):
    """Calculate the effective saving rates for each period"""
    base_rate = config['saving_rate'] - config['order_fee']

    if config['closing_fee_total'] > 0:
        closing_fees = np.minimum(
            np.cumsum(config['saving_rate'] * config['closing_fee_rate']),
            config['closing_fee_total']
        )
        return base_rate - closing_fees
    else:
        return np.full(num_periods, base_rate)


def run_simulation(config: Dict) -> pd.DataFrame:
    """Simulate the savings plan for all possible investment windows"""
    stock_data = download_stock_data(config['stock_id'])
    scaled_prices = scale_price_data(stock_data,
                                           1 + config['annual_return'] -
                                           config['annual_management_fee'])

    investment_days = config['investment_period_years'] * 365
    windows = pd.DataFrame({
        'Start Date': scaled_prices.index[:-investment_days],
        'End Date': scaled_prices.index[investment_days:]
    })

    # Vectorized calculation
    windows['Final Value'] = windows.apply(
        lambda row: calculate_window_value(
            scaled_prices,
            row['Start Date'],
            row['End Date'],
            config
        ), axis=1
    )

    return windows


def calculate_window_value(prices, start_date, end_date, config):
    """Helper function for vectorized calculation"""
    try:
        return simulate_savings(
            prices=prices,
            start_date=start_date,
            end_date=end_date,
            config=config
        )
    except KeyError:
        return np.nan