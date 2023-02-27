"""Functions for cleaning the data sets."""

import os
import zipfile
from functools import reduce

import numpy as np
import pandas as pd


def load_data_files(data_files, dest_dir=None):
    """Load data set.

    Args:
        datafiles (dict): A dictionary with multiple paths for data sets.
        dest_dir (optional, str): A path where unzipped data is stored. Default value is None.

    Returns:
        dictionary: The loaded pandas.DataFrame(s) stored in a dictionary.

    """
    dataframes = {}
    for file_name, file_path in data_files.items():
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == ".csv":
            header_num = 0
            while True:
                try:
                    df = pd.read_csv(file_path, header=header_num)
                    if df.shape[1] == 1:
                        header_num += 1
                    else:
                        break
                except:
                    break
            dataframes[file_name] = df
        elif file_extension == ".zip":
            assert (
                dest_dir is not None
            ), "dest_dir must be specified when reading a zip file."
            zip_ref = zipfile.ZipFile(file_path, "r")
            zip_ref.extractall(dest_dir)
            for inner_file in zip_ref.namelist():
                inner_file_path = os.path.join(dest_dir, inner_file)
                if os.path.isfile(inner_file_path):
                    inner_file_extension = os.path.splitext(inner_file_path)[1]
                    if inner_file_extension == ".csv":
                        header_num = 0
                        while True:
                            try:
                                df = pd.read_csv(inner_file_path, header=header_num)
                                if df.shape[1] == 1:
                                    header_num += 1
                                else:
                                    break
                            except:
                                break
                        dataframes[file_name] = df
                    elif inner_file_extension == ".txt":
                        continue
                    else:
                        raise AssertionError(
                            "Unsupported file format in zip archive: Only .csv files are supported.",
                        )
            zip_ref.close()
        else:
            raise AssertionError(
                "Unsupported file format: Only .csv, and .zip files are supported.",
            )
    return dataframes


def clean_data(data, data_info):
    """Clean data set. Information on data columns is stored in
    ``data_management/data_info.yaml``.

    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml. The
            following keys can be accessed:
            - 'variables_to_keep': Names of columns that are keeped in data cleaning step
            - 'column_rename_mapping': Old and new names of columns to be renamend,
                stored in a dictionary with design: {'old_name': 'new_name'}

    Returns:
        pandas.DataFrame: The cleaned data sets in a dictionary.

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


def merge_data(dfs, index):
    """Merge data sets.

    Args:
        dfs (dict): A dictionary containing the dataframes to be merged.
        index (str): The column to use as the merge key.

    Returns:
        pandas.DataFrame: The merged data set.

    """
    dataframes = list(dfs.values())
    df = reduce(lambda left, right: pd.merge(left, right, on=index), dataframes)
    df = df.set_index(index)
    df = df[df.index <= "2022-10-01"]
    return df


def calculateGrowthRate(data, variable):
    """Calculate growth rates.

    Args:
        data (pandas.DataFrame): The data set.
        variable (str): The variable name for which growth rates are calculated.

    Returns:
        pandas.DataFrame: The data set with growth rates instead of level variable.

    """
    growthRate = data[variable].pct_change(periods=1) * 100
    data[variable] = growthRate
    data = data.dropna(axis=0)
    return data


def calculateDeTrend(data, variable):
    """Detrend a time series data using linear regression.

    Args:
        data (pandas.DataFrame): The data set.
        variable (str): The variable which needs to be detrended.

    Returns:
        pandas.DataFrame: The data set with the detrended variable.

    """
    trend = np.arange(len(data[variable]))
    coeffs = np.polyfit(trend, data[variable], 1)
    trend = np.polyval(coeffs, trend)
    detrended = data[variable] - trend
    data[variable] = detrended
    return data


def calculateExpectations(data, variable):
    """Calculate backward looking expectations.

    Args:
        data (pandas.DataFrame): The data set.
        variable (str): The variable name for which expectations are calculated.

    Returns:
        pandas.DataFrame: The data set with backward looking expectations in a new column.

    """
    data["Backward_Expectations_" + variable] = 0.25 * (
        data[variable].shift(1)
        + data[variable].shift(2)
        + data[variable].shift(3)
        + data[variable].shift(4)
    )
    data = data.dropna(axis=0)
    return data
