"""Test python script."""

import numpy as np
import pandas as pd
import pytest
from nkpc_estimation.config import TEST_DIR
from nkpc_estimation.data_management.clean_data import (
    calculate_backward_expectations,
    calculate_detrend,
    calculate_growth_rates,
    clean_data,
    load_data_files,
    merge_data,
    read_csv_file,
)
from nkpc_estimation.utilities import read_yaml


@pytest.fixture()
def setup():
    out = {
        "data_files": {
            "zip": TEST_DIR / "data_management" / "sample_data" / "data_fixture.zip",
        },
        "dest_dir": TEST_DIR / "data_management" / "sample_data",
    }
    return out


def test_load_zip_files(tmp_path):
    """Test that the function unzips and loads CSV files correctly from a ZIP file."""
    data_files = {
        "data": TEST_DIR / "data_management" / "sample_data" / "data_fixture.zip",
    }
    dest_dir = tmp_path
    dataframes = load_data_files(data_files=data_files, dest_dir=dest_dir)
    assert len(dataframes) == 1
    assert isinstance(dataframes["data"], pd.DataFrame)


def test_unsupported_file_extension():
    """Test that the function raises an error if an unsupported file format is
    specified."""
    data_files = {
        "data": TEST_DIR / "data_management" / "sample_data" / "data_fixture.xlsx",
    }
    with pytest.raises(
        ValueError,
        match="Unsupported file format: Only .csv and .zip files are supported.",
    ):
        load_data_files(data_files=data_files)


def test_load_data_files_missing_dest_dir_for_zip_file_extraction():
    """Test that the function raises specific AssertionError."""
    data_files = {
        "data": TEST_DIR / "data_management" / "sample_data" / "data_fixture.zip",
    }
    with pytest.raises(
        ValueError,
        match="dest_dir must be specified when reading a zip file.",
    ):
        load_data_files(data_files=data_files)


@pytest.fixture()
def example_data_1():
    data1 = pd.DataFrame(
        {
            "index": ["2022-01-01", "2022-02-01", "2022-03-01"],
            "A": [1, 2, 3],
        },
    )
    data2 = pd.DataFrame(
        {
            "index": ["2022-01-01", "2022-02-01", "2022-03-01"],
            "B": [4, 5, 6],
        },
    )
    data3 = pd.DataFrame(
        {
            "index": ["2022-01-01", "2022-02-01", "2022-03-01"],
            "C": [7, 8, 9],
        },
    )
    return {"data1": data1, "data2": data2, "data3": data3}


def test_merge_data(example_data_1):
    """Test if function returns pandas.DataFrame, if index is set correctly, if merged
    data set has correct columns, if merged data set has expected values, if function
    works for a dictionary with only one data frame, and if the function raises an
    exception for non-existent index column."""
    result = merge_data(data=example_data_1, index="index")
    assert isinstance(result, pd.DataFrame)
    ##
    expected_index = pd.to_datetime(["2022-01-01", "2022-02-01", "2022-03-01"])
    assert (result.index == expected_index).all()
    ##
    expected_columns = ["A", "B", "C"]
    assert set(result.columns) == set(expected_columns)
    ##
    expected_values = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    assert result.values.tolist() == expected_values
    ##
    with pytest.raises(KeyError):
        merge_data(data=example_data_1, index="nonexistent_column")


@pytest.fixture()
def example_data():
    return pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})


def test_calculate_growth_rate(example_data):
    """Test if function returns pandas.DataFrame, if variable has expected name, if
    variable has expected values, and if function raises an exception for non-numeric
    input."""
    result = calculate_growth_rates(data=example_data, variable="A")
    assert isinstance(result, pd.DataFrame)
    ##
    expected_column_name = "A"
    assert expected_column_name in result.columns
    ##
    expected_values = [2, 3, 4, 5]
    assert result[expected_column_name].tolist() == expected_values


def test_calculate_detrend(example_data):
    """Test if function returns pandas.DataFrame, if variable has expected name, and if
    function raises an exception for non-numeric input."""
    result = calculate_detrend(data=example_data, variable="A")
    assert isinstance(result, pd.DataFrame)
    ##
    expected_column_name = "A"
    assert expected_column_name in result.columns
    ##
    with pytest.raises(KeyError):
        calculate_detrend(data=example_data, variable="C")


def test_calculate_expectations(example_data):
    """Test if function returns pandas.DataFrame, if new column has expected name, if
    new column has expected values, and if function drops rows with NaN values."""
    result = calculate_backward_expectations(data=example_data, variable="A")
    assert isinstance(result, pd.DataFrame)
    ##
    expected_column_name = "Backward_Expectations_A"
    assert expected_column_name in result.columns
    ##
    expected_values = [1.0, 1.5, 2.0, 2.5, 3.5]
    assert result[expected_column_name].tolist() == expected_values
    ##
    assert result.shape == (5, 3)


def test_clean_data(tmp_path):
    dfs = {
        "GDP": TEST_DIR / "data_management" / "sample_data" / "data_fixture.csv",
        "NAIRU": TEST_DIR / "data_management" / "sample_data" / "data_fixture.zip",
    }
    data_info = read_yaml(
        TEST_DIR / "data_management" / "sample_data" / "data_info_fixture.yaml",
    )
    dfs = load_data_files(
        data_files=dfs,
        dest_dir=tmp_path,
    )
    cleaned_data_dict = clean_data(data=dfs, data_info=data_info)
    # Check that data is cleaned as expected
    assert isinstance(cleaned_data_dict, dict)
    assert len(cleaned_data_dict) == len(dfs)
    assert all(key in cleaned_data_dict for key in dfs)
    for key, _df in cleaned_data_dict.items():
        assert isinstance(cleaned_data_dict[key]["TIME"][0], pd.Timestamp)
        assert all(cleaned_data_dict["GDP"]["GDP"] == np.log(dfs["GDP"]["GDP"]))


def test_merge_data(tmp_path):
    dfs = {
        "GDP": TEST_DIR / "data_management" / "sample_data" / "data_fixture.csv",
        "Emp": TEST_DIR / "data_management" / "sample_data" / "data_fixture.zip",
    }
    data_info = read_yaml(
        TEST_DIR / "data_management" / "sample_data" / "data_info_fixture.yaml",
    )
    dfs = load_data_files(
        data_files=dfs,
        dest_dir=tmp_path,
    )
    cleaned_data = clean_data(data=dfs, data_info=data_info)
    merged_data = merge_data(data=cleaned_data, index="TIME")
    assert isinstance(merged_data, pd.DataFrame)
    assert merged_data.index.name == "TIME"
    for col in dfs:
        assert col in merged_data.columns


def test_read_csv_file():
    file_path = TEST_DIR / "data_management" / "sample_data" / "data_fixture.csv"

    # Test that the function returns a DataFrame
    result = read_csv_file(file_path)
    assert isinstance(result, pd.DataFrame)

    # Test that the function raises an exception for a non-existent file
    with pytest.raises(ValueError):
        read_csv_file("nonexistent_file.csv")
