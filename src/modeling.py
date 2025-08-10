# src/modeling.py

"""
Modeling and Forecasting Module.

This module contains functions for training and evaluating time series models.
It supports both statistical models (ARIMA) and deep learning models (LSTM)
to forecast future asset prices. All experiments are logged using MLflow.
"""

import pandas as pd
import numpy as np
import logging
import joblib
import mlflow
from pmdarima import auto_arima
from typing import Tuple

# Deep learning dependencies
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

from src import config

def _create_sequences(data: np.ndarray, n_steps: int) -> Tuple[np.ndarray, np.ndarray]:
    """Helper function to create time series sequences for LSTM."""
    X, y = [], []
    for i in range(len(data) - n_steps):
        X.append(data[i:i + n_steps])
        y.append(data[i + n_steps])
    return np.array(X), np.array(y)

def train_and_log_arima_model(train_data: pd.Series, test_data: pd.Series):
    """
    Trains an ARIMA model using `auto_arima` and logs the experiment to MLflow.

    The function automatically determines the best ARIMA parameters and
    evaluates the model's performance on a test set, logging metrics
    like MAE, RMSE, and MAPE.

    Args:
        train_data (pd.Series): The training data for model fitting.
        test_data (pd.Series): The unseen test data for evaluation.

    Returns:
        pmdarima.ARIMA: The trained ARIMA model.
    """
    with mlflow.start_run(run_name="ARIMA_Model_Training"):
        logging.info("Training ARIMA model with `auto_arima`...")
        model = auto_arima(train_data, suppress_warnings=True,
                           stepwise=True, seasonal=False)
        
        # Log model parameters
        mlflow.log_param("model_type", "ARIMA")
        mlflow.log_param("arima_order", model.order)

        # Make predictions on the test set
        predictions = model.predict(n_periods=len(test_data))
        
        # Evaluate model performance
        mae = mean_absolute_error(test_data, predictions)
        rmse = np.sqrt(mean_squared_error(test_data, predictions))
        mape = mean_absolute_percentage_error(test_data, predictions)

        # Log metrics to MLflow
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mape", mape)
        
        logging.info(f"ARIMA Model Metrics - MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}")

        # Save the model artifact
        joblib.dump(model, f"{config.REPORTS_DIR}/arima_model.pkl")
        mlflow.log_artifact(f"{config.REPORTS_DIR}/arima_model.pkl")

    return model

def train_and_log_lstm_model(train_data: pd.Series, test_data: pd.Series):
    """
    Trains a TensorFlow LSTM model and logs the experiment to MLflow.

    This function preprocesses the data for the LSTM network, builds a simple
    sequential model, trains it, and evaluates its performance on the test set,
    logging metrics to MLflow.

    Args:
        train_data (pd.Series): The training data for model fitting.
        test_data (pd.Series): The unseen test data for evaluation.

    Returns:
        tensorflow.keras.Model: The trained LSTM model.
    """
    with mlflow.start_run(run_name="LSTM_Model_Training"):
        logging.info("Training LSTM model...")
        
        # Preprocess data for LSTM
        scaler = MinMaxScaler(feature_range=(-1, 1))
        train_scaled = scaler.fit_transform(train_data.values.reshape(-1, 1))
        test_scaled = scaler.transform(test_data.values.reshape(-1, 1))

        X_train, y_train = _create_sequences(train_scaled, config.LSTM_N_STEPS)
        X_test, y_test = _create_sequences(test_scaled, config.LSTM_N_STEPS)
        
        # Reshape data for LSTM input
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        # Build LSTM model
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(config.LSTM_N_STEPS, 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        
        # Train model
        model.fit(X_train, y_train, epochs=config.LSTM_EPOCHS, batch_size=config.LSTM_BATCH_SIZE, verbose=0)
        
        # Make predictions and inverse transform
        y_pred_scaled = model.predict(X_test)
        y_pred = scaler.inverse_transform(y_pred_scaled)
        y_test_original = test_data.iloc[config.LSTM_N_STEPS:].values.reshape(-1, 1)

        # Evaluate model performance
        mae = mean_absolute_error(y_test_original, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test_original, y_pred))
        mape = mean_absolute_percentage_error(y_test_original, y_pred)
        
        # Log metrics to MLflow
        mlflow.log_param("model_type", "LSTM")
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mape", mape)

        logging.info(f"LSTM Model Metrics - MAE: {mae:.2f}, RMSE: {rmse:.2f}, MAPE: {mape:.2f}")

        # Save the model artifact
        model.save(f"{config.REPORTS_DIR}/lstm_model.h5")
        # mlflow.log_artifact(f"{config.REPORTS_DIR}/lstm_model.h5")

    return model

def get_forecast(model, data: pd.Series, periods: int = config.FORECAST_PERIODS) -> Tuple[float, pd.Series, pd.DataFrame]:
    """
    Generates a forecast and calculates the expected annual return.

    This function works with either an ARIMA or an LSTM model. It uses the
    full historical dataset to generate a forward-looking forecast.

    Args:
        model: The trained ARIMA or LSTM model.
        data (pd.Series): The full historical data for the asset.
        periods (int): The number of future periods (days) to forecast.

    Returns:
        Tuple[float, pd.Series, pd.DataFrame]: A tuple containing the expected
        annual return, the forecast series, and the confidence intervals.
    """
    logging.info(f"Generating a {periods}-day forecast...")

    if hasattr(model, 'predict'):
        # ARIMA model
        forecast_result = model.predict(n_periods=periods, return_conf_int=True)
        forecast = pd.Series(forecast_result[0], index=pd.date_range(data.index[-1], periods=periods + 1, freq='B')[1:])
        conf_int = pd.DataFrame(forecast_result[1], index=forecast.index, columns=['lower', 'upper'])
    else:
        # LSTM model
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))
        
        last_sequence = scaled_data[-config.LSTM_N_STEPS:]
        forecast_list = []
        for _ in range(periods):
            prediction = model.predict(last_sequence.reshape(1, config.LSTM_N_STEPS, 1), verbose=0)
            forecast_list.append(prediction[0, 0])
            last_sequence = np.append(last_sequence[1:], prediction, axis=0)

        forecast = pd.Series(scaler.inverse_transform(np.array(forecast_list).reshape(-1, 1)).flatten(),
                             index=pd.date_range(data.index[-1], periods=periods + 1, freq='B')[1:])
        conf_int = None # Confidence intervals are not standard for this simple LSTM setup

    # Calculate expected annual return from the forecast
    start_price = data.iloc[-1]
    end_price_forecast = forecast.iloc[-1]
    annual_return = (end_price_forecast / start_price) ** (252 / periods) - 1

    return annual_return, forecast, conf_int