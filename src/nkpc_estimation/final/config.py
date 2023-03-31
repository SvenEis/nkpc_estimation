"""Configuration of the plots."""

from nkpc_estimation.analysis.config import _DATES, _FEATURE_1, _FEATURE_2, _MODELS
from nkpc_estimation.config import BLD

PLOTS = {
    f"{feature_name_1}_{feature_name_2}_{model_name}": {
        "model": model_name,
        "feature_1": feature_name_1,
        "feature_2": feature_name_2,
    }
    for model_name in _MODELS
    for feature_name_1 in _FEATURE_1
    for feature_name_2 in _FEATURE_2
}

PLOTS_SENSITIVITY = {
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


def path_to_plots(feature_name_1, feature_name_2, model_type):
    return (
        BLD
        / "python"
        / "figures"
        / f"{feature_name_1}_{feature_name_2}_{model_type}.pdf"
    )


def path_to_sensitivity_plots(feature_name_1, feature_name_2, model_type, date):
    return (
        BLD
        / "python"
        / "figures"
        / f"{feature_name_1}_{feature_name_2}_{model_type}_{date}.pdf"
    )


TABLES = {
    f"{feature_name_1}_{feature_name_2}_{model_name}": {
        "model": model_name,
        "feature_1": feature_name_1,
        "feature_2": feature_name_2,
    }
    for model_name in _MODELS
    for feature_name_1 in _FEATURE_1
    for feature_name_2 in _FEATURE_2
}

TABLES_SENSITIVITY = {
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


def path_to_tables(feature_name_1, feature_name_2, model_type):
    return (
        BLD
        / "python"
        / "tables"
        / f"{feature_name_1}_{feature_name_2}_{model_type}.tex"
    )


def path_to_sensitivity_tables(feature_name_1, feature_name_2, model_type, date):
    return (
        BLD
        / "python"
        / "tables"
        / f"{feature_name_1}_{feature_name_2}_{model_type}_{date}.tex"
    )
