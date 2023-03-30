"""Functions plotting results."""

import numpy as np
import plotly.graph_objs as go


def plot_regression(model, x1, x2, y, x1axis_title, x2axis_title, yaxis_title):
    """Plot regression results.

    Args:
        model (statsmodels.base.model.Results): The fitted model.
        x1: variable for x-axis.
        x2: variable for y-axis.
        y: variable for z-axis.
        x1axis_title (str): title of x-axis.
        x2axis_title (str): title of y-axis.
        yaxis_title (str): title of z-axis.

    Returns:
        plotly.scatter.Figure: The figure.

    """
    fig = go.Figure(
        data=[go.Scatter3d(x=x1, y=x2, z=y, mode="markers", marker={"color": "blue"})],
    )
    x_range = np.linspace(x1.min(), x1.max(), 20)
    y_range = np.linspace(x2.min(), x2.max(), 20)
    xx, yy = np.meshgrid(x_range, y_range)
    zz = model.predict(np.column_stack((xx.flatten(), yy.flatten()))).reshape(xx.shape)
    fig.add_trace(go.Surface(x=xx, y=yy, z=zz))
    fig.update_layout(
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
