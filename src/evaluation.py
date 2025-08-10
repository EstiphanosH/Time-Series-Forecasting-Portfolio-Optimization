"""
Handles model performance evaluation.
"""
import logging
from typing import Dict

import numpy as np
import pandas as pd
from pmdarima.arima import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_model(model: ARIMA, test_data: pd.Series) -> Dict[str, float]:
    """Evaluates the forecasting model on the test set."""
    logging.info("--- Evaluation: Assessing model accuracy on test data ---")
    predictions = model.predict(n_periods=len(test_data))
    
    mae = mean_absolute_error(test_data, predictions)
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    
    logging.info(f"Model Test MAE: {mae:.4f}")
    logging.info(f"Model Test RMSE: {rmse:.4f}")
    
    return {"MAE": mae, "RMSE": rmse}