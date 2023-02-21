"""Tasks running the core analyses."""

import pandas as pd
import pytask

from nkpc_estimation.analysis.config import ESTIMATIONS, path_to_estimation_result
from nkpc_estimation.analysis.model import fit_model
from nkpc_estimation.config import BLD


def _create_parametrization(estimations):
    id_to_kwargs = {}
    depends_on = BLD / "python" / "data" / "data_clean.csv"
    for name, config in estimations.items():
        produces = path_to_estimation_result(
            config["outcome"],
            config["feature"],
            config["model"],
        )
        id_to_kwargs[name] = {
            "depends_on": depends_on,
            "model": config["model"],
            "produces": produces,
        }

    return id_to_kwargs


_ID_TO_KWARGS = _create_parametrization(ESTIMATIONS)

for id_, kwargs in _ID_TO_KWARGS.items():

    @pytask.mark.task(id=id_, kwargs=kwargs)
    def task_fit_model_python(depends_on, model, produces):
        """Fit a OLS regression model.

        Args:
            depends_on (dict): Dependencies for the pytask function.
            produces (Path): Path where the outcome is saved.

        Returns:
            Pickle: Saves pickle files in the produces path.

        """
        data = pd.read_csv(depends_on)
        outcome_vars = {
            "BackExp": data["Inflation"] - data["Backward_Expectations_Inflation"],
            "MSC": data["Inflation"] - data["MSC"],
        }
        feature_vars = {
            "Unemp": data["Unemployment"],
            "Unemp_Gap": data["Unemployment"] - data["NAIRU"],
            "Labor_share": data["Labor_share"],
        }
        model_type = "OLS"
        for outcome_name, outcome_var in outcome_vars.items():
            for feature_name, feature_var in feature_vars.items():
                model = fit_model(outcome_var, feature_var, model_type=model_type)
                model.save(
                    f"{produces.parent}/{outcome_name}_{feature_name}_{model_type}.pickle",
                )
