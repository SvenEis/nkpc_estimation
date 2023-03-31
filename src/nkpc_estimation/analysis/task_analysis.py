"""Tasks running the core analyses."""

import pandas as pd
import pytask

from nkpc_estimation.analysis.config import (
    ESTIMATIONS,
    SENSITIVITY,
    path_to_estimation_result,
    path_to_sensitivity_result,
)
from nkpc_estimation.analysis.model import fit_model
from nkpc_estimation.analysis.sensitivity import break_point_analysis
from nkpc_estimation.config import BLD


def _create_parametrization(estimations):
    """Create parametrization for pytask.

    Args:
        estimations (dict): A dictionary with the configuration to create the parametrization.

    Returns:
        dict: A dictionary with the dependencies, model, and information where the output is saved.

    """
    id_to_kwargs = {}
    depends_on = BLD / "python" / "data" / "data_clean.csv"
    for name, config in estimations.items():
        produces = path_to_estimation_result(
            config["feature_1"],
            config["feature_2"],
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
        data = pd.read_csv(depends_on, index_col="TIME")
        outcome_var = data["Inflation"]
        feature_vars_1 = {
            "Unemp": data["Unemployment"],
            "Unemp_Gap": data["Unemployment"] - data["NAIRU"],
            "Labor_share": data["Labor_share"],
            "GDP": data["GDP"],
        }
        feature_vars_2 = {
            "BackExp": data["Backward_Expectations_Inflation"],
            "MSC": data["MSC"],
        }
        model_type = "OLS"
        models = fit_model(
            outcome_var,
            feature_vars_1,
            feature_vars_2,
            model_type=model_type,
        )
        for model_key, model_value in models.items():
            feature_name_1, feature_name_2 = model_key.split(", ")
            model_value.save(
                f"{produces.parent}/{feature_name_1}_{feature_name_2}_{model_type}.pickle",
            )


def _create_parametrization_sensitivity(sensitivity):
    """Create parametrization for pytask.

    Args:
        sensitivity (dict): A dictionary with the configuration to create the parametrization.

    Returns:
        dict: A dictionary with the dependencies, model, and information where the output is saved.

    """
    id_to_kwargs = {}
    depends_on = BLD / "python" / "data" / "data_clean.csv"
    for name, config in sensitivity.items():
        produces = path_to_sensitivity_result(
            config["feature_1"],
            config["feature_2"],
            config["model"],
            config["date"],
        )
        id_to_kwargs[name] = {
            "depends_on": depends_on,
            "model": config["model"],
            "produces": produces,
        }

    return id_to_kwargs


_ID_TO_KWARGS_SENSITIVITY = _create_parametrization_sensitivity(SENSITIVITY)

for id_, kwargs in _ID_TO_KWARGS_SENSITIVITY.items():

    @pytask.mark.task(id=id_, kwargs=kwargs)
    def task_sensitivity_analysis(depends_on, model, produces):
        """Breakpoint analysis of OLS regression model.

        Args:
            depends_on (dict): Dependencies for the pytask function.
            produces (Path): Path where the outcome is saved.

        Returns:
            Pickle: Saves pickle files in the produces path.

        """
        data = pd.read_csv(depends_on, index_col="TIME")
        outcome_var = data["Inflation"]
        feature_vars_1 = {
            "Unemp": data["Unemployment"],
            "Unemp_Gap": data["Unemployment"] - data["NAIRU"],
            "Labor_share": data["Labor_share"],
            "GDP": data["GDP"],
        }
        feature_vars_2 = {
            "BackExp": data["Backward_Expectations_Inflation"],
            "MSC": data["MSC"],
        }

        break_points = ["1984-10-01", "2007-07-01", "2013-01-01", "2020-04-01"]
        model_type = "OLS"
        combined_dict = feature_vars_1 | feature_vars_2

        break_point_analysis(data, outcome_var, combined_dict, break_points)

        dates_ols = [
            "1961-04-01",
            "1984-10-01",
            "2007-07-01",
            "2013-01-01",
            "2020-04-01",
        ]

        for date in dates_ols:
            data_break_point = data[data.index >= date]
            outcome_var = data_break_point["Inflation"]
            feature_vars_1 = {
                "Unemp": data_break_point["Unemployment"],
                "Unemp_Gap": data_break_point["Unemployment"]
                - data_break_point["NAIRU"],
                "Labor_share": data_break_point["Labor_share"],
                "GDP": data_break_point["GDP"],
            }
            feature_vars_2 = {
                "BackExp": data_break_point["Backward_Expectations_Inflation"],
                "MSC": data_break_point["MSC"],
            }

            models = fit_model(
                outcome_var,
                feature_vars_1,
                feature_vars_2,
                model_type=model_type,
            )
            for model_key, model_value in models.items():
                feature_name_1, feature_name_2 = model_key.split(", ")
                model_value.save(
                    f"{produces.parent}/{feature_name_1}_{feature_name_2}_{model_type}_sensitivity_{date}.pickle",
                )
