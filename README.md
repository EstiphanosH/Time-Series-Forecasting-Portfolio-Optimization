# **GMF Investments: Portfolio Optimization Engine**

**A production-grade platform for data-driven investment strategy, forecasting, and risk analysis.**

\<p align="center"\>  
\<a href="https://github.com/GMF-Investments/portfolio-optimization/actions/workflows/ci.yml"\>  
\<img src="https://github.com/GMF-Investments/portfolio-optimization/actions/workflows/ci.yml/badge.svg" alt="CI Pipeline Status"\>  
\</a\>  
\<a href="https://www.python.org/"\>  
\<img src="https://img.shields.io/badge/python-3.10-blue.svg" alt="Python Version"\>  
\</a\>  
\<a href="https://black.readthedocs.io/en/stable/"\>  
\<img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: Black"\>  
\</a\>  
\<a href="https://opensource.org/licenses/MIT"\>  
\<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"\>  
\</a\>  
\</p\>

## **🚀 Overview**

This repository provides a comprehensive, end-to-end analytics engine designed to enhance portfolio management at GMF Investments. It moves beyond traditional analysis by integrating **time series forecasting** with **Modern Portfolio Theory (MPT)** to deliver forward-looking, optimized investment strategies.

The entire platform is built on MLOps best practices, ensuring that every analysis is **robust, reproducible, and ready for production deployment.**

## **✨ Core Features**

| Feature                     | Description                                                                                                                                                             | Technology Stack                                                                 |
| :---- | :---- | :---- |
| 📊 **Interactive Dashboard** | A user-friendly web application for real-time scenario analysis, portfolio optimization, and backtesting without writing a single line of code.                               | Streamlit, Plotly                                                           |
| 🔮 **Predictive Forecasting**   | Utilizes an ARIMA model to generate statistically-grounded forecasts of asset performance, providing a forward-looking edge over historical-only analysis.             | pmdarima, statsmodels                                                       |
| ⚖️ **Efficient Optimization** | Applies Modern Portfolio Theory to calculate the optimal asset allocation for maximizing risk-adjusted returns (Sharpe Ratio) based on the forecast.                   | PyPortfolioOpt                                                                 |
| ⏪ **Dynamic Backtesting**   | Simulates strategy performance with realistic, periodic rebalancing to validate the effectiveness of the model-driven portfolio against industry benchmarks.               | pandas, numpy                                                               |
| 📦 **Containerized & Reproducible** | The entire application is packaged in a **Docker** container, guaranteeing a consistent and error-free environment on any machine, from an analyst's laptop to the cloud. | Docker                                                                         |
| 🔬 **Experiment Tracking**     | Every model training run is logged with **MLflow**, creating a full audit trail of parameters, performance metrics, and model artifacts for governance and comparison.   | MLflow                                                                         |
| 🛡️ **Automated CI/CD**         | A **GitHub Actions** workflow automatically tests, lints, and validates all code changes, ensuring the platform remains stable, reliable, and high-quality.               | GitHub Actions, pytest, flake8                                             |

## **⚡ Quickstart: Running the Interactive Dashboard**

Get the most powerful feature of this platform running in under 60 seconds.

**Prerequisites:** You must have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

1. **Clone the Repository:**  
   git clone https://github.com/EstiphanosH/Time-Series-Forecasting-Portfolio-Optimization.git  
   cd Time-Series-Forecasting-Portfolio-Optimization

2. Build the Docker Image:  
   This command packages the entire application. It only needs to be run once.  
   docker build \-t portfolio-optimizer .

3. **Launch the Dashboard:**  
   docker run \--rm \-p 8501:8501 portfolio-optimizer streamlit run dashboard/app.py

4. Access the Dashboard:  
   Open your web browser and navigate to http://localhost:8501.

You can now interactively build and test portfolio strategies.

## **🛠️ For Developers & Analysts**

While the dashboard is the primary interface, developers and analysts can leverage the full suite of tools for deeper research and automated analysis.

### **Local Environment Setup**

\# 1\. Create and activate a Python 3.10 virtual environment  
python3 \-m venv venv  
source venv/bin/activate

\# 2\. Install all dependencies  
make install

### **Workflow Commands**

This project uses a Makefile to provide simple, memorable commands for common tasks.

| Command             | Description                                                                                             |
| :---- | :---- |
| make run           | Executes the entire automated pipeline (data \-\> model \-\> reports) from the command line.                 |
| make notebook     | Launches the JupyterLab environment for deep-dive exploratory analysis in the /notebooks directory.     |
| make test         | Runs the complete quality assurance suite: formats code with black, lints with flake8, and runs unit tests with pytest. |
| make clean         | Removes all generated artifacts (reports, logs, caches) for a clean slate.                               |
| make mlflow-ui     | Launches the MLflow UI to browse and compare model experiments.                                       |

## **📂 Repository Structure**

The project follows a professional, modular structure for clarity and scalability.

.  
├── .github/  
│   └── workflows/  
│       └── ci.yml             \# Defines the automated CI/CD pipeline using GitHub Actions.  
├── dashboard/  
│   └── app.py                 \# The interactive Streamlit web application.  
├── data/  
│   └── raw/  
│       └── .gitkeep           \# Placeholder for raw data storage.  
├── docs/  
│   └── CRISP-DM.md            \# Documentation mapping the project to the CRISP-DM workflow.  
├── notebooks/  
│   ├── 01\_EDA.ipynb           \# Notebook for Exploratory Data Analysis.  
│   ├── 02\_Forecasting.ipynb   \# Notebook for developing and evaluating the forecasting model.  
│   ├── 03\_Portfolio\_Optimization.ipynb \# Notebook for applying MPT and finding optimal weights.  
│   └── 04\_Backtesting.ipynb   \# Notebook for validating the final strategy.  
├── reports/  
│   ├── figures/               \# Output directory for all generated plots and visualizations.  
│   ├── results/               \# Output directory for serialized objects.  
│   └── final\_report.pdf       \# The generated, professional PDF summary.  
├── scripts/  
│   ├── generate\_report.py     \# Script to automatically create the final PDF report.  
│   └── run\_pipeline.py        \# Main script to execute the end-to-end automated workflow.  
├── src/  
│   ├── \_\_init\_\_.py            \# Makes 'src' a Python package.  
│   ├── backtest.py            \# Contains logic for dynamic backtesting with rebalancing.  
│   ├── config.py              \# Central configuration file for all parameters.  
│   ├── data\_ingestion.py      \# Handles fetching, cleaning, and preprocessing of financial data.  
│   ├── evaluation.py          \# Functions for evaluating model accuracy.  
│   ├── modeling.py            \# Handles model training and forecasting with MLflow integration.  
│   ├── portfolio.py           \# Contains logic for portfolio optimization.  
│   └── utils.py               \# Utility functions for plotting, logging, and file handling.  
├── tests/  
│   └── test\_data\_ingestion.py \# Unit tests for core data processing functions.  
├── .dockerignore  
├── .gitignore  
├── CONTRIBUTING.md            \# Guidelines for developers who want to contribute.  
├── Dockerfile                 \# Defines the containerized environment.  
├── LICENSE  
├── Makefile                   \# Provides simple commands for common tasks.  
├── README.md                  \# The main entry point and documentation for the project.  
└── requirements.txt           \# A list of all Python dependencies.

## **📄 License**

This project is licensed under the **MIT License**. For more details, see the LICENSE file.