"""Functions plotting results."""

import plotly.express as px


def plot_regression(data, x, y, xaxis_title, yaxis_title):
    """Plot regression results.

    Args:
        data (pandas.DataFrame): The data set.
        x: variable for x-axis.
        y: variable for y-axis.
        xaxis_title (str): title of x-axis.
        yaxis_title (str): title of y-axis.

    Returns:
        plotly.scatter.Figure: The figure.

    """
    fig = px.scatter(data, x=x, y=y, trendline="ols")
    fig.update_layout(
        title="",  # Empty title
        xaxis_title=xaxis_title,  # x-axis labeling
        yaxis_title=yaxis_title,  # y-axis labeling
        plot_bgcolor="whitesmoke",
    )
    return fig
