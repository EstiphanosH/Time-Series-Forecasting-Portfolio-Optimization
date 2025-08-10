# tests/test_data_ingestion.py

import pandas as pd
import pytest
import sys
import os

# Ensure the app's source code is accessible to the test runner
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_ingestion import split_data

def test_split_data_correctness():
    """
    Ensures data is split correctly based on the provided split date.
    The 'train' set should contain all data before the split date, and the 'test'
    set should contain all data on or after it.
    """
    dates = pd.to_datetime(pd.date_range(start="2023-01-01", periods=100, freq='D'))
    data = pd.Series(range(100), index=dates, name="TestSeries")
    split_date = "2023-03-01"

    train, test = split_data(data, split_date)

    assert not train.empty, "Train set should not be empty"
    assert not test.empty, "Test set should not be empty"
    assert train.index.max() < pd.to_datetime(split_date), "Max train date should be before split date"
    assert test.index.min() >= pd.to_datetime(split_date), "Min test date should be on or after split date"

def test_split_data_edge_cases():
    """
    Tests splitting behavior with an empty series and with a date that results
    in an empty test set, ensuring the function doesn't crash.
    """
    # Test with an empty series
    empty_series = pd.Series(dtype=float)
    train, test = split_data(empty_series, "2023-01-01")
    assert train.empty, "Train set should be empty for an empty input series"
    assert test.empty, "Test set should be empty for an empty input series"

    # Test with no data after split date
    dates = pd.to_datetime(pd.date_range(start="2023-01-01", periods=10, freq='D'))
    data = pd.Series(range(10), index=dates, name="TestSeries")
    train, test = split_data(data, "2024-01-01")
    assert not train.empty, "Train set should contain all data if split date is in the future"
    assert test.empty, "Test set should be empty if split date is in the future"