"""Configuration of the analysis."""

from nkpc_estimation.config import BLD

_MODELS = ["OLS"]
_FEATURE_1 = ["Unemp", "Unemp_Gap", "Labor_share"]
_FEATURE_2 = ["BackExp", "MSC"]
_DATES = ["1961-04-01", "1984-10-01", "2007-07-01", "2013-01-01", "2020-04-01"]

ESTIMATIONS = {
    f"{feature_name_1}_{feature_name_2}_{model_name}": {
        "model": model_name,
        "feature_1": feature_name_1,
        "feature_2": feature_name_2,
    }
    for model_name in _MODELS
    for feature_name_1 in _FEATURE_1
    for feature_name_2 in _FEATURE_2
}

SENSITIVITY = {
    f"{feature_name_1}_{feature_name_2}_{model_name}_{date}": {
        "model": model_name,
        "feature_1": feature_name_1,
        "feature_2": feature_name_2,
        "date": date,
    }
    for model_name in _MODELS
    for feature_name_1 in _FEATURE_1
    for feature_name_2 in _FEATURE_2
    for date in _DATES
}


def path_to_estimation_result(feature_name_1, feature_name_2, model_type):
    return (
        BLD
        / "python"
        / "models"
        / f"{feature_name_1}_{feature_name_2}_{model_type}.pickle"
    )


def path_to_sensitivity_result(feature_name_1, feature_name_2, model_type, date):
    return (
        BLD
        / "python"
        / "models"
        / f"{feature_name_1}_{feature_name_2}_{model_type}_sensitivity_{date}.pickle"
    )
