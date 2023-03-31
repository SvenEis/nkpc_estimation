"""Tests for the sensitivity analysis."""

import pandas as pd
from nkpc_estimation.analysis.sensitivity import break_point_analysis


def test_break_point_analysis():
    # Create a sample data set with a known break point
    df = pd.DataFrame(
        {"x1": range(10), "x2": range(10), "y": [0, 1, 2, 3, 4, 5, 9, 8, 7, 6]},
    )
    time = pd.date_range("2022-01-01", periods=len(df), freq="D")
    # Set the time variable as the index of the DataFrame
    df = df.set_index(time)
    outcome_variable = df["y"]
    feature_variables = {"x1": df["x1"], "x2": df["x2"]}
    dates = ["2022-01-06"]

    # Test that the function returns a dictionary
    result = break_point_analysis(df, outcome_variable, feature_variables, dates)
    assert isinstance(result, dict)
