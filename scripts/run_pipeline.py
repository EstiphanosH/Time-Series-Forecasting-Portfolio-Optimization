# scripts/run_pipeline.py

"""
Main Automated Pipeline Script for the GMF Portfolio Optimization Engine.

This script orchestrates the entire end-to-end workflow by calling the
specialized modules from the `src` package. It follows the CRISP-DM
methodology to ensure a structured and logical flow.

Workflow:
1.  Setup & Configuration
2.  Data Ingestion & Understanding (Fetch/Clean/Analyze Stationarity & Risk Metrics)
3.  Data Preparation (Split into Train/Test)
4.  Modeling (Train ARIMA and LSTM Models and log with MLflow)
5.  Forecasting (Generate future price predictions)
6.  Evaluation (Assess model accuracy)
7.  Application (Optimize portfolio with the forecast)
8.  Validation (Backtest the final strategy)
9.  Reporting (Generate final reports and figures)

This script is designed to be executed by the main CLI (`main.py`) or
by an automated system like a CI/CD pipeline.
"""

import logging
from typing import Dict, Any
import sys
import os
import joblib

# Ensure the 'src' directory is in the Python path to allow for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import (
    backtest, 
    config, 
    data_ingestion, 
    evaluation, 
    modeling, 
    portfolio, 
    utils
)

def main():
    """
    Executes the entire data science pipeline from data ingestion to report generation.
    """
    
    # 1. Setup
    utils.setup_logging()
    report_metrics: Dict[str, Any] = {}
    
    try:
        # -----------------------------------------------------------------
        # PHASE 1 & 2: BUSINESS & DATA UNDERSTANDING
        # -----------------------------------------------------------------
        logging.info("--- PIPELINE START: Ingesting and Understanding Data ---")
        
        # Ingest data (will use live or synthetic based on config.py)
        all_data = data_ingestion.get_data()
        
        # Perform EDA, risk analysis, and generate plots for each asset
        eda_reports = {}
        for asset in config.TICKERS:
            # We need a separate dataframe for each asset for risk analysis
            asset_df = all_data.rename(columns={asset: 'Close'})
            metrics = data_ingestion.perform_eda_and_risk_analysis(asset_df[[asset]], asset, config.REPORTS_DIR)
            eda_reports[asset] = metrics

            # Save EDA plots
            utils.plot_and_save(utils.plot_prices, asset_df, filename=f"{asset}_price_trends.png")

        # Perform and log stationarity tests on the primary asset
        data_ingestion.check_stationarity(all_data, config.FORECAST_ASSET)
        
        report_metrics['EDA and Risk Metrics'] = eda_reports

        # -----------------------------------------------------------------
        # PHASE 3: DATA PREPARATION
        # -----------------------------------------------------------------
        logging.info("--- PIPELINE: Preparing Data for Modeling ---")
        
        asset_data = all_data[config.FORECAST_ASSET]
        train_data, test_data = data_ingestion.split_data(asset_data, config.TRAIN_TEST_SPLIT_DATE)
        
        # -----------------------------------------------------------------
        # PHASE 4: MODELING & FORECASTING
        # -----------------------------------------------------------------
        logging.info("--- PIPELINE: Training Forecasting Models with MLflow ---")
        
        # Train ARIMA model
        arima_model = modeling.train_and_log_arima_model(train_data, test_data)
        
        # Train LSTM model
        lstm_model = modeling.train_and_log_lstm_model(train_data, test_data)
        
        # Save the best model (e.g., ARIMA for this pipeline) for the dashboard
        # joblib.dump(arima_model, f"{config.REPORTS_DIR}/arima_model.pkl")
        
        # Generate the final forecast using the trained model on the full dataset
        annual_return, forecast, conf_int = modeling.get_forecast(arima_model, asset_data)
        
        # Visualize the forecast
        utils.plot_and_save(
            utils.plot_forecast, 
            asset_data['2023':],  # Plot recent history for better visualization
            forecast, 
            conf_int, 
            filename="forecast_plot.png"
        )
        report_metrics['Forecasted Annual Return (TSLA)'] = f"{annual_return:.2%}"
        
        # -----------------------------------------------------------------
        # PHASE 5: EVALUATION (Part 1: Model Accuracy)
        # -----------------------------------------------------------------
        logging.info("--- PIPELINE: Evaluating Model Accuracy ---")
        
        # The accuracy metrics were already logged by MLflow, but we can capture them here for the report
        arima_metrics = evaluation.evaluate_model(arima_model, test_data)
        lstm_metrics = evaluation.evaluate_model(lstm_model, test_data)
        report_metrics['ARIMA Model Accuracy'] = arima_metrics
        report_metrics['LSTM Model Accuracy'] = lstm_metrics
        
        # -----------------------------------------------------------------
        # APPLICATION & EVALUATION (Part 2: Portfolio & Backtesting)
        # -----------------------------------------------------------------
        logging.info("--- PIPELINE: Optimizing Portfolio and Backtesting Strategy ---")
        
        # Use the forecast to optimize the portfolio
        weights, ef_model = portfolio.optimize_portfolio(all_data, annual_return, config.FORECAST_ASSET)
        utils.plot_and_save(utils.plot_efficient_frontier, ef_model, filename="efficient_frontier.png")
        report_metrics['Optimal Portfolio Weights'] = {k: f"{v:.1%}" for k, v in weights.items()}
        
        # Run a dynamic rolling backtest to validate the strategy
        # This function now uses the model to re-optimize at each step, a key improvement
        cumulative_returns = backtest.run_dynamic_backtest(
            all_data, 
            arima_model, 
            config.REBALANCE_FREQUENCY,
            config.BENCHMARK_WEIGHTS,
        )
        backtest_results = backtest.analyze_backtest_performance(cumulative_returns)
        utils.plot_and_save(utils.plot_backtest, cumulative_returns, filename="backtest_performance.png")
        report_metrics['Backtest Results'] = backtest_results
        
        # -----------------------------------------------------------------
        # PHASE 6: DEPLOYMENT (Reporting)
        # -----------------------------------------------------------------
        logging.info("--- PIPELINE: Generating Final Reports ---")
        
        # Save the final summary report
        utils.save_report(report_metrics, f"{config.REPORTS_DIR}/summary_report.txt")
        
        # Call the new PDF generation script
        from scripts import generate_report
        generate_report.generate_pdf_report(report_metrics, f"{config.REPORTS_DIR}/summary_report.pdf")
        
        logging.info("--- PIPELINE FINISHED SUCCESSFULLY ---")

    except Exception as e:
        logging.error(f"PIPELINE FAILED: An unexpected error occurred: {e}", exc_info=True)
        # Exit with a non-zero status code to indicate failure, useful for CI/CD
        sys.exit(1)

if __name__ == "__main__":
    main()