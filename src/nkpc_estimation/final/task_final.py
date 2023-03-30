"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask
from statsmodels.iolib.summary2 import summary_col

from nkpc_estimation.analysis.config import (
    path_to_estimation_result,
)
from nkpc_estimation.analysis.model import load_model
from nkpc_estimation.config import BLD
from nkpc_estimation.final import plot_regression
from nkpc_estimation.final.config import PLOTS, TABLES, path_to_plots, path_to_tables


def _create_plot_parametrization(plots):
    """Create pytask parametrization for plotting.

    Args:
        plots

    Returns:
        statsmodels.base.model.Results: The fitted model.

    """
    id_to_kwargs = {}
    for name, config in plots.items():
        depends_on = {
            "data": BLD / "python" / "data" / "data_clean.csv",
            "model": path_to_estimation_result(
                config["feature_1"],
                config["feature_2"],
                config["model"],
            ),
        }
        produces = path_to_plots(
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


_ID_TO_KWARGS = _create_plot_parametrization(PLOTS)

for id_, kwargs in _ID_TO_KWARGS.items():

    @pytask.mark.task(id=id_, kwargs=kwargs)
    def task_plot_regression(depends_on, model, produces):
        data = pd.read_csv(depends_on["data"])
        outcome_var = data["Inflation"]
        feature_vars_1 = {
            "Unemp": data["Unemployment"],
            "Unemp_Gap": data["Unemployment"] - data["NAIRU"],
            "Labor_share": data["Labor_share"],
        }
        feature_vars_2 = {
            "BackExp": data["Backward_Expectations_Inflation"],
            "MSC": data["MSC"],
        }
        yaxis_title = "Inflation (in %)"
        x1axis_titles = {
            "Unemp": "Unemployment Rate (in %)",
            "Unemp_Gap": "Unemployment Gap (in %)",
            "Labor_share": "NFB Labor Income Share (in %)",
        }

        x2axis_titles = {
            "BackExp": "Backward Expectation (in %)",
            "MSC": "MSC Expectation (in %)",
        }

        for feature_name_1, feature_var_1 in feature_vars_1.items():
            for feature_name_2, feature_var_2 in feature_vars_2.items():
                x1axis_title = x1axis_titles[feature_name_1]
                x2axis_title = x2axis_titles[feature_name_2]
                model = load_model(depends_on["model"])
                fig = plot_regression(
                    model,
                    feature_var_1,
                    feature_var_2,
                    outcome_var,
                    x1axis_title,
                    x2axis_title,
                    yaxis_title,
                )
                fig.write_image(
                    f"{produces.parent}/{feature_name_1}_{feature_name_2}_OLS.pdf",
                )


def _create_table_parametrization(tables):
    id_to_kwargs = {}
    for name, config in tables.items():
        depends_on = path_to_estimation_result(
            config["feature_1"],
            config["feature_2"],
            config["model"],
        )
        produces = path_to_tables(
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


_ID_TO_KWARGS = _create_table_parametrization(TABLES)

for id_, kwargs in _ID_TO_KWARGS.items():

    @pytask.mark.task(id=id_, kwargs=kwargs)
    def task_create_results_table_python(depends_on, model, produces):
        """Create TeX tables of estimation results.

        Args:
            depends_on: Dependencies for the pytask function.
            model:
            produces: Path where the outcome is saved.

        Returns:
            latex table: A latex table with the regression results.

        """
        model = load_model(depends_on)
        table = summary_col([model], stars=True, float_format="%0.2f").as_latex()
        with open(produces, "w") as f:
            f.writelines(table)
