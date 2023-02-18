"""Functions for fitting the regression model."""

import statsmodels.api as sm
from statsmodels.iolib.smpickle import load_pickle


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
        model = sm.OLS(outcome_variable, feature_variables).fit()
    else:
        message = "Only 'OLS' or 'IV' model_type is supported."
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
