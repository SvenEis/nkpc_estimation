"""Tasks for managing the data."""

import pytask

from nkpc_estimation.config import BLD, SRC
from nkpc_estimation.data_management.clean_data import (
    calculate_backward_expectations,
    calculate_detrend,
    calculate_growth_rates,
    clean_data,
    load_data_files,
    merge_data,
)
from nkpc_estimation.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
        "data": {
            "CPI": SRC / "data" / "DP_LIVE_29012023114147131.csv",
            "Emp": SRC / "data" / "DP_LIVE_29012023134946209.csv",
            "MSC": SRC / "data" / "sca-table32-on-2023-Feb-12.csv",
            "NAIRU": SRC / "data" / "55022-2023-02-Historical-Economic-Data.zip",
            "GDP": SRC / "data" / "GDP.csv",
            "Labor_share": SRC / "data" / "PRS85006173.csv",
        },
    },
)
@pytask.mark.produces(
    {
        "clean_data": BLD / "python" / "data" / "data_clean.csv",
        "unzipped_path": BLD / "python" / "data",
    },
)
def task_clean_data_python(depends_on, produces):
    """Clean the data.

    Args:
        depends_on (dict): Dependencies for the pytask function.
        produces (dict): Path where the outcome is saved.

    Returns:
        csv: The cleaned data set as a csv file.

    """
    data_info = read_yaml(path=depends_on["data_info"])
    dfs = load_data_files(
        data_files=depends_on["data"],
        dest_dir=produces["unzipped_path"],
    )
    dfs = clean_data(data=dfs, data_info=data_info)
    dfs = merge_data(data=dfs, index="TIME")
    dfs = calculate_detrend(data=dfs, variable="GDP")
    dfs = calculate_growth_rates(data=dfs, variable="CPI")
    dfs = dfs.rename(columns=data_info["column_rename_mapping"])
    dfs = calculate_backward_expectations(data=dfs, variable="Inflation")
    dfs.to_csv(produces["clean_data"], index=True)
