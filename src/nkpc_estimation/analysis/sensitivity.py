"""Functions for the sensitivity analysis of the regression model."""

import chow_test as ct
import numpy as np

from nkpc_estimation.analysis.model import fit_model


def break_point_analysis(data, outcome_variable, feature_variables, dates):
    """Test for break point and fit model to data.

    Args:
        data (pandas.DataFrame): The data set.
        outcome_variable: The outcome variable of the regression.
        feature_variables (list): A list of feature variables for the regression.
        dates (list): A list of break point dates.

    Returns:
        statsmodels.base.model.Results: The fitted model.

    """
    for date in dates:
        chowtest = ct.chow_test(
            X_series=outcome_variable,
            y_series=feature_variables,
            last_index=data.index.get_loc(date),
            first_index=data.index.get_loc(date) + 1,
            significance=0.05,
        )
        p_value = chowtest[1]
        if p_value < 0.05:
            dummy_name = f"dummy_{dates}"
            data[dummy_name] = np.where(data.index > date, 1, 0)
            new_feature_variables = [feature_variables, data[dummy_name]]
            model = fit_model(outcome_variable, new_feature_variables, model_type="OLS")

    return model
