"""Functions for fitting the regression model."""

import numpy as np
import statsmodels.api as sm
from statsmodels.iolib.smpickle import load_pickle
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan


def fit_model(outcome_variable, feature_variables, model_type):
    """Fit a model model to data.

    Args:
        data (pandas.DataFrame): The data set.
        outcome_variable: The outcome variable of the regression.
        feature_variables (list): A list of feature variables for the regression.
        model_type (str): Type of regression.

    Returns:
        statsmodels.base.model.Results: The fitted model.

    """
    if model_type == "OLS":
        feature_centered = feature_variables - np.mean(feature_variables)
        model = sm.OLS(outcome_variable, feature_centered).fit()
        BG = acorr_breusch_godfrey(model, nlags=4, store=False)
        BP = het_breuschpagan(model.resid, feature_centered)
        if BG[1] < 0.05 or BP[1] < 0.05:
            model = sm.OLS(outcome_variable, feature_centered).fit(
                cov_type="HAC",
                cov_kwds={"maxlags": 4},
            )
        else:
            model = sm.OLS(outcome_variable, feature_centered).fit()
    else:
        message = "Only 'OLS' model_type is supported."
        raise ValueError(message)

    return model


def load_model(path):
    """Load statsmodels model.

    Args:
        path (str or pathlib.Path): Path to model file.

    Returns:
        statsmodels.base.model.Results: The stored model.

    """
    return load_pickle(path)
