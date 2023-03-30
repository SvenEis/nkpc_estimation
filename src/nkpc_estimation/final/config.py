"""Configuration of the plots."""

from nkpc_estimation.analysis.config import _FEATURE_1, _FEATURE_2, _MODELS
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


def path_to_plots(feature_name_1, feature_name_2, model_type):
    return (
        BLD
        / "python"
        / "figures"
        / f"{feature_name_1}_{feature_name_2}_{model_type}.pdf"
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


def path_to_tables(feature_name_1, feature_name_2, model_type):
    return (
        BLD
        / "python"
        / "tables"
        / f"{feature_name_1}_{feature_name_2}_{model_type}.tex"
    )
