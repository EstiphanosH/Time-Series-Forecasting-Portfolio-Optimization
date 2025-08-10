# src/config.py

"""
Central Configuration File for the GMF Portfolio Optimization Engine.

This file centralizes all constants, file paths, and model parameters, allowing for
easy adjustments to the pipeline's behavior without modifying the core source code.
It acts as the single source of truth for all configurable aspects of the project.
"""

from typing import List, Dict

# -----------------------------------------------------------------
# Data Source Configuration
# -----------------------------------------------------------------
# This flag controls the source of the data for the entire pipeline.
#
# - Set to True: Use locally generated synthetic data. Ideal for offline
#   development, rapid testing, and CI/CD pipelines as it's fast and
#   requires no internet connection.
#
# - Set to False: Fetch live, real-world data from the yfinance API.
#   This is the setting for production analysis and stakeholder reports.
USE_SYNTHETIC_DATA: bool = False


# -----------------------------------------------------------------
# Project Directories & Paths
# -----------------------------------------------------------------
# Defines the folder structure for all inputs and outputs.
REPORTS_DIR: str = "reports"
FIGURES_DIR: str = f"{REPORTS_DIR}/figures"
RESULTS_DIR: str = f"{REPORTS_DIR}/results"
MODEL_PATH: str = f"{RESULTS_DIR}/arima_model.pkl"
SUMMARY_REPORT_PATH: str = f"{REPORTS_DIR}/summary_report.txt"
LOG_PATH: str = f"{REPORTS_DIR}/pipeline.log"


# -----------------------------------------------------------------
# Data Ingestion Parameters
# -----------------------------------------------------------------
# The list of stock/ETF tickers to be analyzed and included in the portfolio.
TICKERS: List[str] = ['TSLA', 'SPY', 'BND']

# The historical time period for data analysis.
START_DATE: str = '2015-07-01'
END_DATE: str = '2025-07-31'


# -----------------------------------------------------------------
# Data Preparation and Modeling
# -----------------------------------------------------------------
# The chronological split date for creating training and testing datasets.
# All data before this date is used for training the model.
# All data on or after this date is used for evaluating the model.
TRAIN_TEST_SPLIT_DATE: str = '2024-08-01'

# The primary high-growth, high-volatility asset to be forecasted by the model.
FORECAST_ASSET: str = 'TSLA'

# The number of periods (in business days) to forecast into the future.
# 252 is approximately one business year.
FORECAST_PERIODS: int = 252


# -----------------------------------------------------------------
# Backtesting Configuration
# -----------------------------------------------------------------
# A traditional, static portfolio to serve as a benchmark for comparison.
# This represents a common, passive investment strategy.
BENCHMARK_WEIGHTS: Dict[str, float] = {'SPY': 0.60, 'BND': 0.40, 'TSLA': 0.0}

# The assumed annual risk-free rate used for calculating the Sharpe Ratio.
# This typically reflects the yield on a short-term government bond (e.g., T-bill).
RISK_FREE_RATE: float = 0.02

# The frequency for rebalancing the portfolio in the dynamic backtest.
# This setting makes the simulation more realistic by accounting for periodic
# adjustments back to the target weights.
# Common values: 'M' (Month End), 'Q' (Quarter End), 'A' (Year End).
REBALANCE_FREQUENCY: str = 'Q'