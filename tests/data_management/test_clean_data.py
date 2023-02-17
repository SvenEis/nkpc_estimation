"""Test python script."""

import pandas as pd
import pytest
from nkpc_estimation.config import TEST_DIR
from nkpc_estimation.data_management.clean_data import load_data_files


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
