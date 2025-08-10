# CRISP-DM Workflow Implementation

This document details how the project maps to the CRISP-DM framework.

### 1. Business Understanding
-   **Objective**: Enhance portfolio management for GMF Investments by using time series forecasting to optimize asset allocation.
-   **Success Criteria**: The model-driven portfolio strategy must demonstrate superior risk-adjusted returns compared to a 60/40 benchmark portfolio in a historical backtest.
-   **Implementation**: `README.md`, `src/config.py` (defining objectives and assets).

### 2. Data Understanding
-   **Objective**: Source and analyze historical data for TSLA, SPY, and BND to identify trends, seasonality, and statistical properties.
-   **Tasks**: Fetch data, visualize price series, analyze volatility, test for stationarity.
-   **Implementation**: `src/data_ingestion.py`, `src/utils.py` (plotting functions), `src/data_ingestion.py` (ADF test).

### 3. Data Preparation
-   **Objective**: Clean, preprocess, and structure the data for modeling.
-   **Tasks**: Handle missing values, split data chronologically into training and testing sets.
-   **Implementation**: `src/data_ingestion.py` (handles missing values and data splitting).

### 4. Modeling
-   **Objective**: Develop a predictive model to forecast the future price of the key growth asset (TSLA).
-   **Tasks**: Train an ARIMA model using `pmdarima` to automatically find the best parameters.
-   **Implementation**: `src/modeling.py`.

### 5. Evaluation
-   **Objective**: Assess the model's predictive accuracy and its value to the business.
-   **Tasks**:
    1.  Evaluate the ARIMA model on the unseen test dataset using MAE and RMSE metrics.
    2.  Backtest the final portfolio strategy against a benchmark to evaluate its financial performance (Total Return, Sharpe Ratio).
-   **Implementation**: `src/evaluation.py`, `src/backtest.py`.

### 6. Deployment
-   **Objective**: Integrate the findings into the business process. In this project, "deployment" means delivering a clear, repeatable pipeline and a summary report with actionable insights for financial analysts.
-   **Tasks**: Generate plots, a summary text file, and a well-documented codebase.
-   **Implementation**: `scripts/run_pipeline.py`, `scripts/generate_report.py`, `src/utils.py`.