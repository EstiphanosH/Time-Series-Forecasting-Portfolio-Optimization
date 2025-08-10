# main.py

"""
Main Command-Line Interface (CLI) for the GMF Portfolio Optimization Engine.

This script provides a user-friendly command-line interface to run the entire
analytics pipeline, or specific parts of it, such as the interactive dashboard
or experiment tracking UI.

Built with Typer for a modern, self-documenting CLI experience.
"""

import typer
import uvicorn
import subprocess
from typing_extensions import Annotated

# Create a Typer application
app = typer.Typer(
    name="GMF Portfolio Engine",
    help="A CLI for running financial forecasting, optimization, and backtesting pipelines.",
    add_completion=False,
    no_args_is_help=True,
)

@app.command()
def run_pipeline(
    live_data: Annotated[
        bool, 
        typer.Option(
            "--live-data", 
            help="Use this flag to fetch live data from the yfinance API. Defaults to using synthetic data.",
        ),
    ] = False,
):
    """
    Runs the entire end-to-end data analysis pipeline.
    
    This command will:
    1. Ingest data (either synthetic or live, based on the flag).
    2. Train and evaluate the forecasting model.
    3. Optimize the portfolio based on the forecast.
    4. Run a dynamic backtest of the strategy.
    5. Save all results and figures to the /reports directory.
    """
    print("🚀 Starting the end-to-end pipeline...")
    
    # We dynamically import the script to ensure Typer remains lightweight
    # and to allow the script to be run independently.
    from scripts import run_pipeline as pipeline_script
    from src import config
    
    # Override the config setting based on the CLI flag
    original_setting = config.USE_SYNTHETIC_DATA
    config.USE_SYNTHETIC_DATA = not live_data
    
    print(f"Data Source: {'Live yfinance API' if not config.USE_SYNTHETIC_DATA else 'Local Synthetic Data'}")

    try:
        pipeline_script.main()
        print("\n✅ Pipeline completed successfully!")
    except Exception as e:
        print(f"\n❌ Pipeline failed with an error: {e}")
    finally:
        # Reset the config to its original state to not affect other processes
        config.USE_SYNTHETIC_DATA = original_setting


@app.command()
def dashboard():
    """
    Launches the interactive Streamlit dashboard.
    
    The dashboard provides a user-friendly web interface for real-time
    scenario analysis, optimization, and backtesting.
    """
    print("🚀 Launching the Streamlit dashboard...")
    print("Navigate to http://localhost:8501 in your browser.")
    
    # Use subprocess to run streamlit, as it's a blocking command
    subprocess.run(["streamlit", "run", "dashboard/app.py"])


@app.command()
def mlflow_ui():
    """
    Launches the MLflow UI to track and compare model experiments.
    
    This interface allows you to view model parameters, performance metrics,
    and artifacts from every pipeline run.
    """
    print("🚀 Launching the MLflow UI...")
    print("Navigate to http://localhost:5000 in your browser.")
    
    # Use subprocess for this blocking command as well
    subprocess.run(["mlflow", "ui", "--backend-store-uri", "sqlite:///mlflow.db"])


if __name__ == "__main__":
    app()