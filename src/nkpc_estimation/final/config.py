"""Configuration of the plots."""

import pathlib

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


def path_to_plots(
    feature_name_1: str,
    feature_name_2: str,
    model_type: str,
) -> pathlib.PosixPath:
    """Create the paths for the plots.

    Args:
        feature_name_1 (str): The name of the first independent variable.
        feature_name_2 (str): The name of the second independent variable.
        model_type (str): The name of the estimation method.

    Returns:
        pathlib.PosixPath: The path for the estimation results.

    """
    return (
        BLD
        / "python"
        / "figures"
        / f"{feature_name_1}_{feature_name_2}_{model_type}.pdf"
    )


def path_to_sensitivity_plots(
    feature_name_1: str,
    feature_name_2: str,
    model_type: str,
    date: str,
) -> pathlib.PosixPath:
    """Create the paths for the plots of then sensitivity analysis.

    Args:
        feature_name_1 (str): The name of the first independent variable.
        feature_name_2 (str): The name of the second independent variable.
        model_type (str): The name of the estimation method.
        date (str): The date of the breakpoint.

    Returns:
        pathlib.PosixPath: The path for the tables.

    """
    return (
        BLD
        / "python"
        / "figures"
        / f"{feature_name_1}_{feature_name_2}_{model_type}_{date}.pdf"
    )


def path_to_tables(
    feature_name_1: str,
    feature_name_2: str,
    model_type: str,
) -> pathlib.PosixPath:
    """Create the paths for the tables.

    Args:
        feature_name_1 (str): The name of the first independent variable.
        feature_name_2 (str): The name of the second independent variable.
        model_type (str): The name of the estimation method.

    Returns:
        pathlib.PosixPath: The path for the estimation results.

    """
    return (
        BLD
        / "python"
        / "tables"
        / f"{feature_name_1}_{feature_name_2}_{model_type}.tex"
    )


def path_to_sensitivity_tables(
    feature_name_1: str,
    feature_name_2: str,
    model_type: str,
    date: str,
) -> pathlib.PosixPath:
    """Create the paths for the tables of then sensitivity analysis.

    Args:
        feature_name_1 (str): The name of the first independent variable.
        feature_name_2 (str): The name of the second independent variable.
        model_type (str): The name of the estimation method.
        date (str): The date of the breakpoint.

    Returns:
        pathlib.PosixPath: The path for the tables.

    """
    return (
        BLD
        / "python"
        / "tables"
        / f"{feature_name_1}_{feature_name_2}_{model_type}_{date}.tex"
    )
