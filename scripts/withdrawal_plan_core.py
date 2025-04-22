"""Core functionality for withdrawal plan simulations"""

from datetime import datetime, timedelta
import pandas as pd
from typing import Dict
from scripts.utils import scale_price_data, download_stock_data, calculate_tax


def simulate_withdrawals(
        prices: pd.Series, start_date: datetime,
        end_date: datetime, config: Dict
) -> float:
    portfolio_value = config['initial_portfolio_value']
    cost_basis = config['initial_portfolio_invested'] # Track original
    # investment
    current_date = start_date
    years_last = 0

    while portfolio_value > 0 and current_date < end_date:
        try:
            # Monthly calculations
            next_date = min(current_date + timedelta(days=30), end_date)
            monthly_return = (prices.loc[next_date] / prices.loc[
                current_date]) - 1

            # Inflation-adjusted withdrawal
            withdrawal = config['monthly_withdrawal'] * (
                        1 + config['inflation'] / 12) ** years_last

            # Calculate tax using utils function
            capital_gains_tax = calculate_tax(
                withdrawal_amount=withdrawal,
                tax_rate=config['capital_gains_tax_rate'],
                tax_free_threshold=config.get('tax_free_threshold', 0) / 12,
                cost_basis=cost_basis * (withdrawal / portfolio_value)
            )

            total_withdrawal = withdrawal + capital_gains_tax

            # Update portfolio and cost basis
            portfolio_value -= total_withdrawal
            cost_basis *= (1 - withdrawal / portfolio_value)  # Proportional
            # cost basis
            portfolio_value *= (1 + monthly_return)

            years_last += 1 / 12
            current_date = next_date

        except (KeyError, ZeroDivisionError):
            break

    return min(years_last, config['withdrawal_period_years'])


def run_withdrawal_simulation(config: Dict) -> pd.DataFrame:
    """Run full withdrawal simulation across historical periods"""
    # Download and process data
    raw_data = download_stock_data(config['stock_id'])
    scaled_prices = scale_price_data(
        raw_data,
        1 + config['annual_return'] - config['annual_management_fee']
    )

    # Calculate simulation windows
    max_duration_days = config['withdrawal_period_years'] * 365
    valid_start_dates = scaled_prices.index[:-max_duration_days]

    results = {
        "Start Date": valid_start_dates,
        "Years Lasted": [
            simulate_withdrawals(
                scaled_prices,
                start,
                start + timedelta(days=max_duration_days),
                config
            )
            for start in valid_start_dates
        ]
    }

    return pd.DataFrame(results)