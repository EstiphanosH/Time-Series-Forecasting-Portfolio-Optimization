# src/data_ingestion.py

"""
Handles all data acquisition tasks for the pipeline.

This module contains functions to fetch, clean, and prepare the financial data.
It includes a switching mechanism to use either live data from the yfinance API
or locally generated synthetic data for development and testing purposes.
"""

import logging
from typing import Tuple

import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.tsa.stattools import adfuller

from src import config  # Import the central configuration module

def _generate_synthetic_data() -> pd.DataFrame:
    """
    Generates a reproducible, synthetic dataset for offline development and testing.
    This creates a random walk process that mimics general market behavior.
    """
    logging.info("Generating SYNTHETIC data for offline use as per config settings.")
    np.random.seed(42)  # for reproducibility
    dates = pd.date_range(start=config.START_DATE, end=config.END_DATE, freq='B')
    df = pd.DataFrame(index=dates)

    for ticker in config.TICKERS:
        # Assign different characteristics to each asset for realism
        if 'BND' in ticker:
            start_price, drift, volatility = 75, 0.00002, 0.005
        elif 'SPY' in ticker:
            start_price, drift, volatility = 200, 0.0004, 0.01
        else:  # For volatile stocks like TSLA
            start_price, drift, volatility = 50, 0.0012, 0.03
        
        random_returns = np.random.randn(len(dates)) * volatility + drift
        price_path = start_price * (1 + random_returns).cumprod()
        df[ticker] = price_path
    
    return df

def _fetch_from_yfinance() -> pd.DataFrame:
    """
    Fetches and cleans real-world financial data from the yfinance API.
    Handles potential missing values by forward- and backward-filling.
    """
    logging.info(f"Fetching REAL data for {config.TICKERS} from yfinance API...")
    try:
        data = yf.download(
            tickers=config.TICKERS,
            start=config.START_DATE,
            end=config.END_DATE
        )['Adj Close']

        if data.empty:
            logging.error("No data fetched from yfinance. Check tickers, dates, and network connection.")
            raise ValueError("yfinance returned an empty DataFrame.")

        # Clean data: Handle missing values common on holidays or data gaps
        data.ffill(inplace=True)  # Propagate last valid observation forward
        data.bfill(inplace=True)  # Fill any remaining NaNs at the beginning
        
        logging.info("Real data fetched and cleaned successfully.")
        return data
    except Exception as e:
        logging.error(f"An error occurred during yfinance data ingestion: {e}")
        raise

def get_data() -> pd.DataFrame:
    """
    Main data acquisition function.
    Acts as a switch to provide either live or synthetic data based on the
    `USE_SYNTHETIC_DATA` flag in the project's configuration file.
    """
    if config.USE_SYNTHETIC_DATA:
        return _generate_synthetic_data()
    else:
        return _fetch_from_yfinance()

def check_stationarity(data: pd.DataFrame, asset: str) -> None:
    """
    Performs and logs the results of the Augmented Dickey-Fuller (ADF) test
    on both the price series and the daily returns to check for stationarity.
    """
    logging.info(f"--- Data Understanding: Stationarity Check for {asset} ---")
    
    price_series = data[asset].dropna()
    adf_result_price = adfuller(price_series)
    logging.info(f"ADF Test on Price Series: p-value = {adf_result_price[1]:.4f}")
    if adf_result_price[1] > 0.05:
        logging.info("Conclusion: Price series is likely NON-STATIONARY (as expected).")
    else:
        logging.info("Conclusion: Price series is likely STATIONARY.")

    returns_series = data[asset].pct_change().dropna()
    adf_result_returns = adfuller(returns_series)
    logging.info(f"ADF Test on Daily Returns: p-value = {adf_result_returns[1]:.4f}")
    if adf_result_returns[1] <= 0.05:
        logging.info("Conclusion: Returns series is likely STATIONARY (as required for ARIMA).")
    else:
        logging.info("Conclusion: Returns series is likely NON-STATIONARY.")

def split_data(data: pd.Series, split_date: str) -> Tuple[pd.Series, pd.Series]:
    """
    Chronologically splits a time series into training and testing sets.
    This preserves the temporal order, which is crucial for valid model evaluation.
    """
    logging.info(f"Splitting data at {split_date} for training and testing.")
    train = data.loc[data.index < split_date]
    test = data.loc[data.index >= split_date]
    logging.info(f"Training set size: {len(train)}, Test set size: {len(test)}")
    return train, test