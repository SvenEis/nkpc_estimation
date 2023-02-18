"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask

from nkpc_estimation.analysis.config import (
    path_to_estimation_result,
)
from nkpc_estimation.analysis.model import load_model
from nkpc_estimation.config import BLD
from nkpc_estimation.final import plot_regression
from nkpc_estimation.final.config import PLOTS, TABLES, path_to_plots, path_to_tables


def _create_plot_parametrization(plots):
    id_to_kwargs = {}
    depends_on = BLD / "python" / "data" / "data_clean.csv"
    for name, config in plots.items():
        produces = path_to_plots(config["outcome"], config["feature"])
        id_to_kwargs[name] = {
            "depends_on": depends_on,
            "produces": produces,
        }

    return id_to_kwargs


_ID_TO_KWARGS = _create_plot_parametrization(PLOTS)

for id_, kwargs in _ID_TO_KWARGS.items():

    @pytask.mark.task(id=id_, kwargs=kwargs)
    def task_plot_regression(depends_on, produces):
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
        xaxis_titles = {
            "Unemp": "Unemployment Rate (in %)",
            "Unemp_Gap": "Unemployment Gap (in %)",
            "Labor_share": "NFB Labor Income Share (in %)",
        }

        yaxis_titles = {
            "BackExp": "$\\pi_{t}- E \\pi^{Back}_{t}$",
            "MSC": "$\\pi_{t}- E \\pi^{MSC}_{t}$",
        }

        for outcome_var in outcome_vars.values():
            for feature_list in feature_vars.values():
                for xaxis_title in xaxis_titles.values():
                    for yaxis_title in yaxis_titles.values():
                        fig = plot_regression(
                            data,
                            feature_list,
                            outcome_var,
                            xaxis_title,
                            yaxis_title,
                        )
                        fig.write_image(produces)


def _create_table_parametrization(tables):
    id_to_kwargs = {}
    for name, config in tables.items():
        depends_on = path_to_estimation_result(config["data"], config["model"])
        produces = path_to_tables(config["data"], config["model"])
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
        """Create TeX tables of estimation results."""
        model = load_model(depends_on)
        table = model.summary().as_latex()
        with open(produces, "w") as f:
            f.writelines(table)
