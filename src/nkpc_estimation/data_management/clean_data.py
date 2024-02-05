"""Functions for cleaning the data sets."""

import os
import pathlib
import zipfile
from functools import reduce

import numpy as np
import pandas as pd


def load_data_files(
    data_files: dict[str, str | pathlib.PosixPath],
    dest_dir: str | None = None,
) -> dict[str, pd.DataFrame]:
    """Load data sets from csv and zip files.

    Args:
        data_files (Dict[str, Union[str, pathlib.PosixPath]]): A dictionary with file names and paths.
        dest_dir (str, optional): The directory where zip files are extracted. Defaults to None.

    Raises:
        ValueError: If the input is not of the expected format.
        FileNotFoundError: If a file is not found.

    Returns:
        Dict[str, pd.DataFrame]: The loaded pandas.DataFrame(s) stored in a dictionary.

    """
    if not isinstance(data_files, dict):
        raise ValueError("data_files must be a dictionary.")

    dataframes = {}
    for file_name, file_path in data_files.items():
        if not isinstance(file_name, str) or not isinstance(
            file_path,
            str | pathlib.PosixPath,
        ):
            raise ValueError(
                "File names and paths must be strings or pathlib.PosixPath objects.",
            )

        file_path_str = str(file_path)
        if not os.path.isfile(file_path_str):
            raise FileNotFoundError(f"File not found: {file_path_str}")

        file_extension = os.path.splitext(file_path_str)[1]
        if file_extension == ".csv":
            df = read_csv_file(file_path_str)
            dataframes[file_name] = df
        elif file_extension == ".zip":
            if dest_dir is None:
                raise ValueError("dest_dir must be specified when reading a zip file.")

            with zipfile.ZipFile(file_path_str, "r") as zip_ref:
                file_list = zip_ref.namelist()
                if "Quarterly_Feb2023.csv" not in file_list:
                    raise ValueError("File not found in zip archive.")
                inner_file_path = os.path.join(dest_dir, "Quarterly_Feb2023.csv")
                zip_ref.extract("Quarterly_Feb2023.csv", dest_dir)
                df = read_csv_file(inner_file_path)
                dataframes[file_name] = df
        else:
            raise ValueError(
                "Unsupported file format: Only .csv and .zip files are supported.",
            )

    return dataframes


def read_csv_file(file_path: str) -> pd.DataFrame:
    """Read a csv file into a pandas DataFrame.

    Args:
        file_path (str): The path to the csv file.

    Raises:
        ValueError: If the csv file cannot be read.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    """
    header_num = 0
    while True:
        try:
            df = pd.read_csv(file_path, header=header_num)
            if df.shape[1] == 1:
                header_num += 1
            else:
                break
        except Exception as e:
            raise ValueError(f"Error reading csv file {file_path}: {e!s}") from e
    return df


def clean_data(
    data: dict[str, pd.DataFrame],
    data_info: dict[str, any],
) -> dict[str, pd.DataFrame]:
    """Clean data set. Information on data columns is stored in
    ``data_management/data_info.yaml``.

    Args:
        data: The data set.
        data_info: Information on data set stored in data_info.yaml. The following keys can be accessed:
            - 'variables_to_keep': Names of columns that are kept in data cleaning step
            - 'dates_to_keep': Names of date columns to be kept
            - 'column_rename_mapping': Old and new names of columns to be renamed, stored in a dictionary with design: {'old_name': 'new_name'}

    Returns:
        The cleaned data sets in a dictionary.

    """
    combined_cols = data_info["variables_to_keep"].copy()
    combined_cols.extend(data_info["dates_to_keep"])

    df_dict = {
        df_name: df[df.columns.intersection(combined_cols)]
        for df_name, df in data.items()
    }

    for key, _value in df_dict.items():
        rename_dict = {col: key for col in data_info["variables_to_keep"]}
        df_dict[key] = _value.rename(columns=rename_dict)
        for date_col in data_info["dates_to_keep"]:
            if (date_col in _value.columns) and date_col in ("DATE", "date"):
                df_dict[key]["TIME"] = df_dict[key].pop(date_col).apply(pd.to_datetime)
            elif (date_col in _value.columns) and date_col == "TIME":
                df_dict[key]["TIME"] = pd.to_datetime(df_dict[key][date_col])
            elif date_col == "Quarter" and (date_col in _value.columns):
                df_dict[key]["TIME"] = pd.to_datetime(
                    df_dict[key]["Year"].astype(str)
                    + "Q"
                    + df_dict[key]["Quarter"].astype(str),
                )
                df_dict[key] = df_dict[key].drop(["Year", "Quarter"], axis=1)
        if key in ("GDP", "Labor_share"):
            df_dict[key][key] = np.log(df_dict[key][key])
    return df_dict


def merge_data(
    data: dict[str, pd.DataFrame],
    index: str,
    end_date: str = "2022-10-01",
) -> pd.DataFrame:
    """Merge data sets.

    Args:
        data (Dict[str, pd.DataFrame]): A dictionary containing the dataframes to be merged.
        index (str): The column to use as the merge key.
        end_date (str, optional): The latest date to include in the merged data set.
            Defaults to "2022-10-01".

    Returns:
        pd.DataFrame: The merged data set.

    Raises:
        ValueError: If the input arguments are not of the expected type.

    """
    # Validate input arguments
    if not isinstance(data, dict):
        raise ValueError("dataframes_dict must be a dictionary.")
    if not isinstance(index, str):
        raise ValueError("merge_key must be a string.")
    if not isinstance(end_date, str):
        raise ValueError("end_date must be a string.")

    dataframes = list(data.values())
    df = reduce(lambda left, right: pd.merge(left, right, on=index), dataframes)
    df = df.set_index(index)
    df = df[df.index <= end_date]
    return df


def calculate_growth_rates(data: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Calculate growth rates for specified variables.

    Args:
        data (pandas.DataFrame): The data set.
        variable (str): The variable name for which growth rate is calculated.

    Returns:
        pandas.DataFrame: The data set with growth rates for specified variables.

    Raises:
        ValueError: If the variable is not found in the `data` dataframe.

    """
    if variable not in data.columns:
        raise ValueError(f"Variable '{variable}' not found in the input dataframe.")

    growthRate = data[variable].pct_change(periods=1) * 100
    data[f"{variable}_growth_rate"] = growthRate
    data = data.dropna(axis=0)
    return data


def calculate_detrend(
    data: pd.DataFrame,
    variable: str,
    order: int = 1,
    detrended_column: str | None = None,
) -> pd.DataFrame:
    """Detrend a time series data using linear regression.

    Args:
        data (pandas.DataFrame): The data set.
        variable (str): The variable which needs to be detrended.
        order (int): The order of the polynomial used for the trend line.
        detrended_column (str, optional): The name of the column to store the detrended data.

    Returns:
        pandas.DataFrame: The data set with the detrended variable.

    Raises:
        ValueError: If the input data has less than two data points.

    """
    if len(data) < 2:
        raise ValueError("Input data must have at least two data points")

    trend = np.arange(len(data[variable]))
    coeffs = np.polyfit(trend, data[variable], order)
    trend = np.polyval(coeffs, trend)
    detrended = data[variable] - trend

    if detrended_column is None:
        detrended_column = f"{variable}_detrended"

    data[detrended_column] = detrended
    return data


def calculate_backward_expectations(
    data: pd.DataFrame,
    variable: str,
    lag_period: int = 4,
) -> pd.DataFrame:
    """Calculate the backward-looking average for a given variable.

    Args:
        data (pd.DataFrame): The input data.
        variable (str): The name of the variable for which expectations are calculated.
        lag_period (int, optional): The number of periods to use for the backward-looking average. Default is 4.

    Returns:
        pd.DataFrame: The input data with a new column containing the backward-looking average.

    """
    expectations = data[variable].rolling(window=lag_period, min_periods=1).mean()
    data[f"Backward_Expectations_{variable}"] = expectations
    return data.dropna(axis=0)
