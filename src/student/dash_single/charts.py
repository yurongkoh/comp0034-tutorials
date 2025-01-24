import pathlib
import pandas as pd
import plotly.express as px


def line_chart(feature):
    """ Creates a line chart with data from paralympics.csv

    Data is displayed over time from 1960 onwards.
    The figure shows separate trends for the winter and summer events.

     Parameters
     feature: events, sports or participants

     Returns
     fig: Plotly Express line figure
     """

    # take the feature parameter from the function and check it is valid
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    else:
        # Make sure it is lowercase to match the dataframe column names
        feature = feature.lower()

    # Read the data from .csv into a DataFrame
    cols = ["type", "year", "host", feature]

    # Uses importlib.resources rather than pathlib.Path
    # path to paralympic data
    path = pathlib.Path(__file__).parent.parent.joinpath("data", "paralympics.csv")
    line_chart_data = pd.read_csv(path, usecols=cols)

    # Create a Plotly Express line chart with the following parameters
    #    line_chart_data is the DataFrame
    #    x="year" is the column to use as the x-axis
    #    y=feature is the column to use as the y-axis
    #    color="type" indicates if winter or summer
    fig = px.line(line_chart_data,
                  x="year",
                  y=feature,
                  color="type",
                  title=f"How has the number of {feature} changed over time?",
                  labels={feature: "", "year": "Year"}
                  )
    return fig
