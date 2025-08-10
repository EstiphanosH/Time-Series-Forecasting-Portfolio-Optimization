# src/portfolio.py

"""
Handles all portfolio optimization tasks using Modern Portfolio Theory (MPT).

This module takes the expected returns and historical price data to calculate
the optimal asset allocation that maximizes the risk-adjusted return (Sharpe Ratio).
"""

import logging
from typing import Dict, Tuple

import pandas as pd
from pypfopt import (
    EfficientFrontier, 
    risk_models, 
    expected_returns
)
# Ensure we type hint the return object correctly
from pypfopt.efficient_frontier import EfficientFrontier as IEfficientFrontier

def optimize_portfolio(
    data: pd.DataFrame, 
    forecast_return: float, 
    forecast_asset: str
) -> Tuple[Dict[str, float], IEfficientFrontier]:
    """
    Calculates the optimal portfolio for the maximum Sharpe ratio.

    This function requires pandas objects with their metadata intact (index and columns)
    to function correctly, especially for plotting.

    Args:
        data (pd.DataFrame): DataFrame of historical asset PRICES.
        forecast_return (float): The forecasted annual return for the key asset.
        forecast_asset (str): The name of the asset being forecasted (e.g., 'TSLA').

    Returns:
        Tuple[Dict[str, float], IEfficientFrontier]: A dictionary of the optimal
        weights and the EfficientFrontier object instance used for plotting.
    """
    logging.info("--- Modeling: Optimizing Portfolio with MPT ---")
    
    # 1. Calculate Expected Annual Returns
    # This function expects a DataFrame of PRICES and returns a pandas Series of
    # mean historical returns, preserving the ticker names in the index.
    # DO NOT use .values here.
    mu = expected_returns.mean_historical_return(data)
    
    # 2. Substitute our forecast for the key asset
    # We modify the pandas Series directly.
    mu[forecast_asset] = forecast_return
    
    # 3. Calculate the Annualized Sample Covariance Matrix
    # This function also expects a DataFrame of PRICES and returns a pandas
    # DataFrame, preserving tickers in both the index and columns.
    # DO NOT use .values here.
    S = risk_models.sample_cov(data)
    
    # 4. Instantiate the EfficientFrontier object
    # The 'ef' object will now contain all necessary metadata for plotting.
    ef = EfficientFrontier(mu, S)
    
    # 5. Find the portfolio that maximizes the Sharpe ratio
    weights = ef.max_sharpe()
    
    # Clean the weights (e.g., round small values to zero)
    cleaned_weights = ef.clean_weights()
    
    logging.info("Optimal portfolio weights calculated:")
    for asset, weight in cleaned_weights.items():
        logging.info(f"  {asset}: {weight:.1%}")
        
    # Log the expected performance of this optimal portfolio
    performance = ef.portfolio_performance(verbose=False)
    logging.info(f"Expected Annual Return: {performance[0]:.2%}")
    logging.info(f"Annual Volatility (Risk): {performance[1]:.2%}")
    logging.info(f"Sharpe Ratio: {performance[2]:.2f}")
    
    return cleaned_weights, ef