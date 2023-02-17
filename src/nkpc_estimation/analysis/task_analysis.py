"""Tasks running the core analyses."""

import pandas as pd
import pytask

from nkpc_estimation.analysis.model import fit_model
from nkpc_estimation.config import BLD


@pytask.mark.depends_on(
    {
        "scripts": ["model.py"],
        "data": BLD / "python" / "data" / "data_clean.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "models")
def task_fit_model_python(depends_on, produces):
    """Fit a OLS regression model.

    Args:
        depends_on (dict): Dependencies for the pytask function.
        produces (Path): Path where the outcome is saved.

    Returns:
        Pickle: Saves pickle files in the produces path.

    """
    data = pd.read_csv(depends_on["data"])
    outcome_vars = {
        "BackExp": data["Inflation"] - data["Backward_Expectations_Inflation"],
        "MSC": data["Inflation"] - data["MSC"],
    }
    feature_vars = {
        "Unemp": data["Unemployment"],
        "Unemp_Gap": data["Unemployment"] - data["NAIRU"],
        "Labor_share": data["Labor_share"],
    }
    model_types = ["OLS"]
    for outcome_name, outcome_var in outcome_vars.items():
        for feature_name, feature_list in feature_vars.items():
            for model_type in model_types:
                model = fit_model(outcome_var, feature_list, model_type)
                model.save(
                    produces / f"{outcome_name}_{feature_name}_{model_type}.pickle",
                )
