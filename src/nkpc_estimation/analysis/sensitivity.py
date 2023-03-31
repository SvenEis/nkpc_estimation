"""Functions for the sensitivity analysis of the regression model."""

import chow_test as ct


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
    pvalues = {}
    for feature_name, feature_var in feature_variables.items():
        pvalues[feature_name] = {}
        for date in dates:
            chowtest = ct.chow_test(
                X_series=outcome_variable,
                y_series=feature_var,
                last_index=data.index.get_loc(date),
                first_index=data.index.get_loc(date) + 1,
                significance=0.05,
            )
            pvalues[feature_name][date] = chowtest[1]
    return pvalues
