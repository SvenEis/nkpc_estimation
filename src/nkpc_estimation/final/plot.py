"""Functions plotting results."""

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import statsmodels


def plot_regression(
    model: statsmodels.base.model.Results,
    x1: pd.Series,
    x2: pd.Series,
    y: pd.Series,
    x1axis_title: str,
    x2axis_title: str,
    yaxis_title: str,
    title: str = None,
) -> plotly.graph_objects.Scatter:
    """Plot regression results.

    Args:
        model (statsmodels.base.model.Results): The fitted model.
        x1 (pandas.Series): variable for x-axis.
        x2 (pandas.Series): variable for y-axis.
        y (pandas.Series): variable for z-axis.
        x1axis_title (str): title of x-axis.
        x2axis_title (str): title of y-axis.
        yaxis_title (str): title of z-axis.

    Returns:
        plotly.graph_objects.Scatter: The figure.

    """
    fig = go.Figure(
        data=[go.Scatter3d(x=x1, y=x2, z=y, mode="markers", marker={"color": "blue"})],
    )
    x_range = np.linspace(x1.min(), x1.max(), 20)
    y_range = np.linspace(x2.min(), x2.max(), 20)
    xx, yy = np.meshgrid(x_range, y_range)
    zz = model.predict(np.column_stack((xx.flatten(), yy.flatten()))).reshape(xx.shape)
    fig.add_trace(go.Surface(x=xx, y=yy, z=zz, showlegend=False))
    fig.update_layout(
        title=title,
        scene={
            "xaxis": {
                "backgroundcolor": "rgb(200, 200, 230)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
                "title": x1axis_title,
                "range": [x1.min(), x1.max()],
            },
            "yaxis": {
                "backgroundcolor": "rgb(230, 200,230)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
                "title": x2axis_title,
                "range": [x2.min(), x2.max()],
            },
            "zaxis": {
                "backgroundcolor": "rgb(230, 230,200)",
                "gridcolor": "white",
                "showbackground": True,
                "zerolinecolor": "white",
                "title": yaxis_title,
            },
        },
        scene_camera={
            "eye": {"x": 2.25, "y": 2.25, "z": 0.1},
            "up": {"x": 0, "y": 0, "z": 1},
            "center": {"x": 0, "y": 0, "z": 0},
            "projection": {"type": "perspective"},
        },
    )

    return fig
