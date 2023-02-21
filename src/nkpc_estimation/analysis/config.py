"""Configuration of the analysis."""

from nkpc_estimation.config import BLD

_MODELS = ["OLS"]
_OUTCOME = ["BackExp", "MSC"]
_FEATURE = ["Unemp", "Unemp_Gap", "Labor_share"]

ESTIMATIONS = {
    f"{outcome_name}_{feature_name}_{model_name}": {
        "model": model_name,
        "outcome": outcome_name,
        "feature": feature_name,
    }
    for model_name in _MODELS
    for outcome_name in _OUTCOME
    for feature_name in _FEATURE
}


def path_to_estimation_result(outcome_name, feature_name, model_type):
    return (
        BLD / "python" / "models" / f"{outcome_name}_{feature_name}_{model_type}.pickle"
    )
