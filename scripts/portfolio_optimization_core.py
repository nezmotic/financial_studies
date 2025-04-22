"""Core functionality for portfolio optimization"""
import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Tuple


def download_asset_data(assets: List[str], start_date: str,
                        end_date: str) -> pd.DataFrame:
    """Download historical price data for multiple assets with validation"""
    assets.sort()

    # Convert input dates to datetime objects
    start_dt = pd.to_datetime(start_date)
    end_dt = pd.to_datetime(end_date)

    # Download data
    data = yf.download(assets, start=start_date, end=end_date)[
        "Close"].dropna()

    # Check if any data exists in requested range
    if data.empty:
        # Check maximum available history
        full_data = yf.download(assets, period="max")["Close"].dropna()

        if full_data.empty:
            raise ValueError(
                f"No historical data available for assets: {assets}")

        # Get actual available dates
        actual_start = full_data.index[0].strftime('%Y-%m-%d')
        actual_end = full_data.index[-1].strftime('%Y-%m-%d')

        raise ValueError(
            f"No data available between {start_date} and {end_date}.\n"
            f"Available data range: {actual_start} to {actual_end}"
        )

    # Get actual dates from downloaded data
    data_start = data.index[0].strftime('%Y-%m-%d')
    data_end = data.index[-1].strftime('%Y-%m-%d')

    # Check if actual range matches requested range
    if (data.index[0] > start_dt) or (data.index[-1] < end_dt):
        print(
            f"Note: Available data in requested range is from {data_start} to {data_end}")

    return data


def calculate_metrics(prices: pd.DataFrame) -> Tuple[pd.Series, pd.DataFrame]:
    """Calculate returns and covariance matrix"""
    returns = prices.pct_change().dropna()
    mean_returns = returns.mean() * 252  # Annualized
    cov_matrix = returns.cov() * 252  # Annualized
    return mean_returns, cov_matrix


def generate_portfolios(num_portfolios: int,
                        mean_returns: pd.Series,
                        cov_matrix: pd.DataFrame,
                        risk_free_rate: float) -> Tuple[
    np.ndarray, List[np.ndarray]]:
    """Generate random portfolios with performance metrics"""
    num_assets = len(mean_returns)
    results = np.zeros((3, num_portfolios))
    weights_list = []

    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= weights.sum()
        ret, risk, sharpe = portfolio_performance(weights, mean_returns,
                                                  cov_matrix, risk_free_rate)

        results[0, i] = ret
        results[1, i] = risk
        results[2, i] = sharpe
        weights_list.append(weights)

    return results, weights_list


def portfolio_performance(weights: np.ndarray,
                          mean_returns: pd.Series,
                          cov_matrix: pd.DataFrame,
                          risk_free_rate: float) -> Tuple[float, float, float]:
    """Calculate portfolio return, risk, and Sharpe ratio"""
    ret = np.dot(weights, mean_returns)
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe = (ret - risk_free_rate) / risk
    return ret, risk, sharpe


def find_optimal_portfolios(results: np.ndarray,
                            weights_list: List[np.ndarray],
                            mean_returns: pd.Series,
                            cov_matrix: pd.DataFrame,
                            risk_free_rate: float) -> dict:
    """Identify optimal portfolios"""
    max_sharpe_idx = results[2].argmax()
    min_risk_idx = results[1].argmin()

    return {
        'max_sharpe': {
            'weights': weights_list[max_sharpe_idx],
            'return': results[0, max_sharpe_idx],
            'risk': results[1, max_sharpe_idx],
            'sharpe': results[2, max_sharpe_idx]
        },
        'min_risk': {
            'weights': weights_list[min_risk_idx],
            'return': results[0, min_risk_idx],
            'risk': results[1, min_risk_idx],
            'sharpe': results[2, min_risk_idx]
        }
    }


def run_optimization(assets: List[str],
                     start_date: str,
                     end_date: str,
                     num_portfolios: int = 10000,
                     risk_free_rate: float = 0.02) -> dict:
    """Main optimization workflow"""
    prices = download_asset_data(assets, start_date, end_date)
    mean_returns, cov_matrix = calculate_metrics(prices)
    results, weights = generate_portfolios(num_portfolios, mean_returns,
                                           cov_matrix, risk_free_rate)
    portfolios = find_optimal_portfolios(results, weights, mean_returns,
                                         cov_matrix, risk_free_rate)

    return {
        'prices': prices,
        'returns': mean_returns,
        'cov_matrix': cov_matrix,
        'simulation_results': results,
        'optimal_portfolios': portfolios
    }