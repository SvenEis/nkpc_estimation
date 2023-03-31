"""Functions for fitting the regression model."""


import pandas as pd
import statsmodels.api as sm
from statsmodels.iolib.smpickle import load_pickle
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan


def fit_model(
    outcome_variable: pd.Series,
    feature_variables: list[pd.Series],
    model_type: str,
) -> sm.base.model.Results:
    """Fit a model to data.

    Args:
        outcome_variable (pandas.Series): The outcome variable of the regression.
        feature_variables (List[pandas.Series]): A list of feature variables for the regression.
        model_type (str): Type of regression. Only 'OLS' model_type is supported.

    Returns:
        statsmodels.base.model.Results: The fitted model.

    """
    if model_type != "OLS":
        raise ValueError("Only 'OLS' model_type is supported.")

    model = sm.OLS(outcome_variable, feature_variables).fit()
    BG_pvalue = acorr_breusch_godfrey(model, nlags=4, store=False)[1]
    BP_pvalue = het_breuschpagan(model.resid, feature_variables)[1]

    if BG_pvalue < 0.05 or BP_value < 0.05:
        model = sm.OLS(outcome_variable, feature_variables).fit(
            cov_type="HAC",
            cov_kwds={"maxlags": 4},
        )
        print(
            f"Refitted model with HAC standard errors (BG p-value={BG_pvalue:.4f}, BP p-value={BP_pvalue:.4f}).",
        )
    else:
        print(
            f"Fitted model with OLS (BG p-value={BG_pvalue:.4f}, BP p-value={BP_pvalue:.4f}).",
        )
    return model


def load_model(path):
    """Load statsmodels model.

    Args:
        path (str or pathlib.Path): Path to model file.

    Returns:
        statsmodels.base.model.Results: The stored model.

    """
    return load_pickle(path)
