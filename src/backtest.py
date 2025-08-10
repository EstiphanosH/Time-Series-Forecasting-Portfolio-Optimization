# src/backtest.py

"""
Backtesting Module.

This module provides functions to simulate a trading strategy's performance
over a historical period. It includes a dynamic rolling backtest that
re-optimizes the portfolio at regular intervals, providing a more realistic
assessment of the strategy.
"""

import pandas as pd
import logging
from typing import Dict
from pypfopt import expected_returns, risk_models, EfficientFrontier

def run_dynamic_backtest(
    all_data: pd.DataFrame, 
    forecasting_model, 
    rebalance_freq: str, 
    benchmark_weights: Dict[str, float]
) -> pd.DataFrame:
    """
    Performs a dynamic rolling backtest of the portfolio strategy.

    This function simulates a live trading scenario by iteratively re-optimizing
    the portfolio based on the latest available data and a new forecast at each
    rebalancing period. It then compares the performance of this strategy against
    a static benchmark portfolio.

    Args:
        all_data (pd.DataFrame): The full historical price data for all assets.
        forecasting_model: The trained model (e.g., ARIMA) to generate new forecasts.
        rebalance_freq (str): The frequency of rebalancing ('M', 'Q', 'A' for monthly, quarterly, annually).
        benchmark_weights (Dict[str, float]): A dictionary of weights for the
                                             benchmark portfolio (e.g., {'SPY': 0.6, 'BND': 0.4}).

    Returns:
        pd.DataFrame: A DataFrame containing the cumulative returns of both the
                      optimized strategy and the benchmark.
    """
    logging.info(f"Starting dynamic rolling backtest with {rebalance_freq} rebalancing...")

    # Calculate daily returns for all assets
    returns = all_data.pct_change().dropna()

    # Create empty DataFrames to store results
    strategy_returns = pd.Series(index=returns.index)
    benchmark_returns = pd.Series(index=returns.index)
    
    # Initialize portfolio values to 1
    strategy_value = 1.0
    benchmark_value = 1.0
    
    rebalance_dates = returns.resample(rebalance_freq).first().index

    for i, date in enumerate(rebalance_dates):
        # Determine the start and end of the current backtesting period
        start_period = date
        end_period = rebalance_dates[i+1] if i < len(rebalance_dates) - 1 else returns.index[-1]
        
        # Use data up to the current rebalance date for optimization
        train_data = returns.loc[:start_period].iloc[:-1]
        
        if len(train_data) < 252:
            logging.warning(f"Not enough data to train at {date}. Skipping rebalance.")
            continue

        # Get a new forecast for the high-growth asset
        from modeling import get_forecast
        annual_return, _, _ = get_forecast(forecasting_model, all_data.loc[:start_period]['TSLA'])

        # Re-optimize the portfolio
        mu = expected_returns.mean_historical_return(train_data, frequency=252)
        mu[config.FORECAST_ASSET] = annual_return
        S = risk_models.sample_cov(train_data, frequency=252)
        
        ef = EfficientFrontier(mu, S)
        optimal_weights = ef.max_sharpe()
        
        # Normalize weights to ensure they sum to 1
        optimal_weights_series = pd.Series(optimal_weights)
        optimal_weights_series /= optimal_weights_series.sum()
        
        # Apply weights to the portfolio for the duration of the rebalance period
        period_returns = returns.loc[start_period:end_period]
        
        strategy_daily_returns = (period_returns * optimal_weights_series).sum(axis=1)
        benchmark_daily_returns = (period_returns * pd.Series(benchmark_weights)).sum(axis=1)

        # Update cumulative returns
        strategy_returns.loc[period_returns.index] = strategy_daily_returns
        benchmark_returns.loc[period_returns.index] = benchmark_daily_returns

    # Calculate cumulative growth from daily returns
    cumulative_returns = pd.DataFrame({
        'Strategy': (1 + strategy_returns).cumprod(),
        'Benchmark': (1 + benchmark_returns).cumprod()
    })
    
    # Fill any NaNs that might have been created by the resampling
    cumulative_returns.ffill(inplace=True)

    return cumulative_returns

def analyze_backtest_performance(cumulative_returns: pd.DataFrame) -> dict:
    """
    Analyzes and calculates key performance metrics from backtest results.

    Args:
        cumulative_returns (pd.DataFrame): A DataFrame with cumulative returns for
                                            the strategy and the benchmark.

    Returns:
        dict: A dictionary containing performance metrics for both portfolios.
    """
    logging.info("Analyzing backtest performance...")
    
    daily_returns = cumulative_returns.pct_change().dropna()
    
    results = {}
    for portfolio in cumulative_returns.columns:
        portfolio_returns = daily_returns[portfolio]
        
        cagr = (cumulative_returns[portfolio].iloc[-1] ** (252 / len(cumulative_returns))) - 1
        volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = cagr / volatility
        
        results[portfolio] = {
            'Cumulative Annual Growth Rate (CAGR)': cagr,
            'Annual Volatility': volatility,
            'Sharpe Ratio': sharpe_ratio
        }

    return results