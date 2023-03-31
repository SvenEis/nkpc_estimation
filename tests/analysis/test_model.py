"""Tests for the regression model."""

import numpy as np
import pandas as pd
import pytest
from nkpc_estimation.analysis.model import fit_model

DESIRED_PRECISION = 10e-2


@pytest.fixture()
def random_data():
    np.random.seed(123)
    n = 100
    outcome = np.random.normal(size=n)
    feature1 = np.random.normal(size=n)
    feature2 = np.random.normal(size=n)
    return pd.DataFrame(
        {
            "outcome_variable": outcome,
            "feature_vars_1": feature1,
            "feature_vars_2": feature2,
            "model_type": "OLS",
        },
    )


def test_fit_model_error_model_type(random_data):
    """Tests if ValueError is raised with incorrect 'model_type'."""
    random_data["model_type"] = "quadratic"
    with pytest.raises(ValueError):
        assert fit_model(**random_data)
