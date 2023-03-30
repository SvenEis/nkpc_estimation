"""Tests for the regression model."""

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm
from nkpc_estimation.analysis.model import fit_model

DESIRED_PRECISION = 10e-2


@pytest.fixture()
def random_data():
    np.random.seed(123)
    n = 100
    outcome = np.random.normal(size=n)
    features = np.random.normal(size=(n, 3))
    return pd.DataFrame(
        {
            "outcome": outcome,
            "feature1": features[:, 0],
            "feature2": features[:, 1],
            "feature3": features[:, 2],
        },
    )


def test_structure_model(random_data):
    """Tests if result is a 'RegressionResultsWrapper' object with non-zero degrees of
    freedom and correct number of parameters."""
    outcome_var = random_data["outcome"]
    feature_vars = random_data[["feature1", "feature2", "feature3"]]
    model = fit_model(outcome_var, feature_vars, "OLS")
    assert isinstance(model, sm.regression.linear_model.RegressionResultsWrapper)
    assert model.df_resid > 0
    assert len(model.params) == feature_vars.shape[1]


def test_model_OLS(random_data):
    """Tests if parameters of function are correct."""
    feature_vars = random_data[["feature1", "feature2", "feature3"]]
    outcome_var = (
        2.00 * random_data["feature1"]
        + 3.00 * random_data["feature2"]
        + 4.00 * random_data["feature3"]
    )
    model = fit_model(outcome_var, feature_vars, "OLS")
    assert np.isclose(model.params["feature1"], 2.0, atol=DESIRED_PRECISION)
    assert np.isclose(model.params["feature2"], 3.0, atol=DESIRED_PRECISION)
    assert np.isclose(model.params["feature3"], 4.0, atol=DESIRED_PRECISION)


def test_fit_model_error_model_type(random_data):
    """Tests if ValueError is raised with incorrect 'model_type'."""
    outcome_var = random_data["outcome"]
    feature_vars = random_data[["feature1", "feature2", "feature3"]]
    with pytest.raises(ValueError):
        assert fit_model(outcome_var, feature_vars, "quadratic")
