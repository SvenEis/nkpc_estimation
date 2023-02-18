"""Configuration of the plots."""

from nkpc_estimation.analysis.config import _FEATURE, _MODELS, _OUTCOME
from nkpc_estimation.config import BLD

PLOTS = {
    f"{outcome_name}_{feature_name}": {"outcome": outcome_name, "feature": feature_name}
    for outcome_name in _OUTCOME
    for feature_name in _FEATURE
}


def path_to_plots(outcome_name, feature_name):
    return BLD / "python" / "figures" / f"{outcome_name}_{feature_name}.pdf"


TABLES = {
    f"{outcome_name}_{feature_name}_{model_name}": {
        "model": model_name,
        "data": [outcome_name, feature_name],
    }
    for model_name in _MODELS
    for outcome_name in _OUTCOME
    for feature_name in _FEATURE
}


def path_to_tables(data, model_type):
    return BLD / "python" / "tables" / f"{data}_{model_type}.tex"
