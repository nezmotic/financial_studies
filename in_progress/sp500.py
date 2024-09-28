import yfinance as yf
import pandas as pd
import numpy as np
import datetime


def fetch_sp500_tickers():
    # Fetch S&P 500 constituent tickers from Wikipedia
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    sp500_table = table[0]
    return sp500_table['Symbol'].tolist()


def get_historical_data(tickers, start_date, end_date):
    # Fetch historical data for given tickers
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']


def calculate_returns(data):
    # Calculate daily returns
    returns = data.pct_change().dropna()
    return returns


def get_outperformers(stock_returns, benchmark_returns):
    # Determine if the stock outperformed the benchmark
    cumulative_stock_return = (1 + stock_returns).prod() - 1
    cumulative_benchmark_return = (1 + benchmark_returns).prod() - 1
    return cumulative_stock_return > cumulative_benchmark_return


def main():
    # Step 1: Get the list of S&P 500 tickers
    sp500_tickers = fetch_sp500_tickers()

    # Include S&P 500 index itself
    sp500_ticker = '^GSPC'
    all_tickers = [sp500_ticker] + sp500_tickers

    # Step 2: Fetch historical data for all tickers
    all_data = get_historical_data(all_tickers, "1900-01-01", "2024-12-31")

    # Separate SP500 data from stock data
    sp500_data = all_data[sp500_ticker]
    stock_data_all = all_data.drop(columns=[sp500_ticker])

    # Store results
    past_outperformers = []
    future_outperformers = []

    # Step 3: Process each stock individually
    for ticker in sp500_tickers:
        try:
            stock_data = stock_data_all[ticker].dropna()

            # Find the overlapping period
            common_start_date = max(stock_data.index[0], sp500_data.index[0])
            common_end_date = min(stock_data.index[-1], sp500_data.index[-1])

            if common_start_date >= common_end_date:
                continue  # No overlapping period

            # Get overlapping data
            stock_data = stock_data.loc[common_start_date:common_end_date]
            sp500_data_period = sp500_data.loc[common_start_date:common_end_date]

            # Split the data into past and future periods
            split_date = common_start_date + (common_end_date - common_start_date) // 2

            past_stock_data = stock_data.loc[:split_date]
            future_stock_data = stock_data.loc[split_date:]

            past_sp500_data = sp500_data_period.loc[:split_date]
            future_sp500_data = sp500_data_period.loc[split_date:]

            # Calculate returns
            past_stock_returns = calculate_returns(past_stock_data)
            future_stock_returns = calculate_returns(future_stock_data)

            past_sp500_returns = calculate_returns(past_sp500_data)
            future_sp500_returns = calculate_returns(future_sp500_data)

            # Determine past outperformers
            if get_outperformers(past_stock_returns, past_sp500_returns):
                past_outperformers.append(ticker)

                # Check future performance of past outperformers
                if get_outperformers(future_stock_returns, future_sp500_returns):
                    future_outperformers.append(ticker)

        except Exception as e:
            print(f"Error processing ticker {ticker}: {e}")
            continue

    # Output the result
    print(f"Number of stocks that outperformed the S&P 500 in the past: {len(past_outperformers)}")
    print(f"Number of these stocks that also outperformed the S&P 500 in the future: {len(future_outperformers)}")
    print("List of stocks that outperformed in both periods:", future_outperformers)


if __name__ == "__main__":
    main()
