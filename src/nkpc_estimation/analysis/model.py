"""Functions for fitting the regression model."""

import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.iolib.smpickle import load_pickle
from statsmodels.stats.diagnostic import acorr_breusch_godfrey, het_breuschpagan


def fit_model(
    outcome_variable: dict[str, pd.Series],
    feature_vars_1: dict[str, pd.Series],
    feature_vars_2: pd.Series,
    model_type: str,
) -> statsmodels.base.model.Results:
    """Fit a model to data.

    Args:
        outcome_variable (pandas.Series): The outcome variable of the regression.
        feature_vars_1 (dict): A dictionary of feature variables for the regression.
        feature_vars_2 (dict): A dictionary of feature variables for the regression.
        model_type (str): Type of regression. Only 'OLS' model_type is supported.

    Returns:
        statsmodels.base.model.Results: The fitted model.

    """
    if model_type != "OLS":
        raise ValueError("Only 'OLS' model_type is supported.")
    models = {}
    for feature_name_1, feature_var_1 in feature_vars_1.items():
        for feature_name_2, feature_var_2 in feature_vars_2.items():
            feature_var = list(zip(feature_var_1, feature_var_2, strict=False))
            model = sm.OLS(outcome_variable, feature_var).fit()
            BG_pvalue = acorr_breusch_godfrey(model, nlags=4, store=False)[1]
            BP_pvalue = het_breuschpagan(model.resid, feature_var)[1]

            if BG_pvalue < 0.05 or BP_pvalue < 0.05:
                model = sm.OLS(outcome_variable, feature_var).fit(
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
            models[f"{feature_name_1}, {feature_name_2}"] = model

    return models


def load_model(path):
    """Load statsmodels model.

    Args:
        path (str or pathlib.Path): Path to model file.

    Returns:
        statsmodels.base.model.Results: The stored model.

    """
    return load_pickle(path)
