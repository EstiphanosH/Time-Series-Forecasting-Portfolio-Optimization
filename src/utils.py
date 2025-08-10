# src/utils.py

"""
Utility functions for logging, file handling, and plotting.
Includes a patch to handle a dependency issue between PyPortfolioOpt and Matplotlib.
"""

import logging
import os
from typing import Dict, Any

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------------
# MONKEY-PATCH for PyPortfolioOpt and Matplotlib compatibility
# ---------------------------------------------------------------------------------
# The PyPortfolioOpt library (as of v1.5.5) attempts to set a deprecated
# matplotlib style ('seaborn-deep') upon import, which causes a FileNotFoundError
# with modern matplotlib versions.
#
# By setting a valid style here BEFORE importing pypfopt.plotting, we prevent
# the library's problematic code from running and causing a crash.
# 'seaborn-v0_8-deep' is the modern equivalent of the style it was trying to use.
plt.style.use('seaborn-v0_8-deep')
# ---------------------------------------------------------------------------------

# Now it is safe to import pypfopt.plotting
from pypfopt import plotting

from src.config import FIGURES_DIR, LOG_PATH, SUMMARY_REPORT_PATH

def setup_logging() -> None:
    """Configures the root logger for the project."""
    # Ensure the handler is clean for multiple runs
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(module)s:%(lineno)d] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_PATH, mode='w') # Overwrite log file on each run
        ]
    )

def save_report(metrics: Dict[str, Any]) -> None:
    """Saves a dictionary of metrics to a text file."""
    with open(SUMMARY_REPORT_PATH, 'w') as f:
        for key, value in metrics.items():
            f.write(f"--- {key} ---\n")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    f.write(f"  {sub_key}: {sub_value}\n")
            else:
                f.write(f"  {value}\n")
            f.write("\n")
    logging.info(f"Summary report saved to {SUMMARY_REPORT_PATH}")

def plot_and_save(plot_func, *args, filename: str, **kwargs) -> None:
    """Generic function to generate and save a plot."""
    try:
        os.makedirs(FIGURES_DIR, exist_ok=True)
        fig, ax = plt.subplots(figsize=(14, 7))
        
        plot_func(*args, ax=ax, **kwargs)
        
        plt.tight_layout()
        plt.grid(True)
        filepath = os.path.join(FIGURES_DIR, filename)
        plt.savefig(filepath)
        plt.close(fig)
        logging.info(f"Plot saved to {filepath}")
    except Exception as e:
        logging.error(f"Failed to create plot {filename}: {e}", exc_info=True)


# --- Specific Plotting Functions ---

def plot_prices(data: pd.DataFrame, ax, **kwargs) -> None:
    ax.plot(data)
    ax.set_title("Historical Adjusted Close Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend(data.columns)

def plot_forecast(data: pd.Series, forecast: pd.Series, conf_int: pd.DataFrame, ax, **kwargs) -> None:
    ax.plot(data, label='Historical Prices')
    ax.plot(forecast, label='Forecast', color='red', linestyle='--')
    ax.fill_between(forecast.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.5, label='95% Confidence Interval')
    ax.set_title(f"{data.name} Price Forecast")
    ax.legend()
    
def plot_efficient_frontier(ef, ax, **kwargs) -> None:
    plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)
    ax.set_title("Efficient Frontier with Optimal Portfolio")

def plot_backtest(cumulative_returns: pd.DataFrame, ax, **kwargs) -> None:
    ax.plot(cumulative_returns)
    ax.set_title("Strategy vs. Benchmark Cumulative Returns")
    ax.set_ylabel("Growth of $1")
    ax.legend(cumulative_returns.columns)