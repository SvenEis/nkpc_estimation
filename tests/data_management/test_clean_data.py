"""Test python script."""

import pandas as pd
import pytest
from nkpc_estimation.config import TEST_DIR
from nkpc_estimation.data_management.clean_data import (
    calculateDeTrend,
    calculateExpectations,
    calculateGrowthRate,
    load_data_files,
    merge_data,
)


def test_load_csv_files():
    """Test that function loads CSV files correctly."""
    data_files = {
        "data": TEST_DIR / "data_management" / "sample_data" / "data_fixture.csv",
    }
    dataframes = load_data_files(data_files)
    assert len(dataframes) == 1
    assert isinstance(dataframes["data"], pd.DataFrame)


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
    dataframes = load_data_files(data_files, dest_dir)
    assert len(dataframes) == 1
    assert isinstance(dataframes["data"], pd.DataFrame)


def test_unsupported_file_extension():
    """Test that the function raises an error if an unsupported file format is
    specified."""
    data_files = {
        "data": TEST_DIR / "data_management" / "sample_data" / "data_fixture.txt",
    }
    with pytest.raises(
        AssertionError,
        match="Unsupported file format: Only .csv, and .zip files are supported.",
    ):
        load_data_files(data_files)


def test_load_data_files_missing_dest_dir_for_zip_file_extraction():
    """Test that the function raises specific AssertionError."""
    data_files = {
        "data": TEST_DIR / "data_management" / "sample_data" / "data_fixture.zip",
    }
    with pytest.raises(
        AssertionError,
        match="dest_dir must be specified when reading a zip file.",
    ):
        load_data_files(data_files)


def test_load_data_files_unsupported_file_in_zip_archive(tmp_path):
    """Test that the function raises specific AssertionError."""
    data_files = {
        "data": TEST_DIR / "data_management" / "sample_data" / "wrong_datatype.zip",
    }
    dest_dir = tmp_path
    with pytest.raises(
        AssertionError,
        match="Unsupported file format in zip archive: Only .csv files are supported.",
    ):
        load_data_files(data_files, dest_dir=dest_dir)


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
    result = merge_data(example_data_1, "index")
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
        merge_data(example_data_1, "nonexistent_column")


@pytest.fixture()
def example_data():
    return pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [10, 20, 30, 40, 50]})


def test_calculateGrowthRate(example_data):
    """Test if function returns pandas.DataFrame, if variable has expected name, if
    variable has expected values, and if function raises an exception for non-numeric
    input."""
    result = calculateGrowthRate(example_data, "A")
    assert isinstance(result, pd.DataFrame)
    ##
    expected_column_name = "A"
    assert expected_column_name in result.columns
    ##
    expected_values = [100.0, 50.0, 33.33333333333333, 25.0]
    assert result[expected_column_name].tolist() == expected_values
    ##
    with pytest.raises(KeyError):
        calculateGrowthRate(example_data, "C")


def test_calculateDeTrend(example_data):
    """Test if function returns pandas.DataFrame, if variable has expected name, and if
    function raises an exception for non-numeric input."""
    result = calculateDeTrend(example_data, "A")
    assert isinstance(result, pd.DataFrame)
    ##
    expected_column_name = "A"
    assert expected_column_name in result.columns
    ##
    with pytest.raises(KeyError):
        calculateDeTrend(example_data, "C")


def test_calculateExpectations(example_data):
    """Test if function returns pandas.DataFrame, if new column has expected name, if
    new column has expected values, and if function drops rows with NaN values."""
    result = calculateExpectations(example_data, "A")
    assert isinstance(result, pd.DataFrame)
    ##
    expected_column_name = "Backward_Expectations_A"
    assert expected_column_name in result.columns
    ##
    expected_values = [2.5]
    assert result[expected_column_name].tolist() == expected_values
    ##
    assert result.shape == (1, 3)
