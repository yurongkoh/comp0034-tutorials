import pathlib
import pandas as pd
import plotly.express as px
import sqlite3
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


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


def bar_gender(event_type):
    """
    Creates a stacked bar chart showing change in the ration of male and female competitors in the summer and winter paralympics.

    Parameters
    event_type: str Winter or Summer

    Returns
    fig: Plotly Express bar chart
    """
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    path = pathlib.Path(__file__).parent.parent.joinpath("data", "paralympics.csv")
    df_events = pd.read_csv(path, usecols=cols)
    # Drop Rome as there is no male/female data
    # Drop rows where male/female data is missing
    df_events = df_events.dropna(subset=['participants_m', 'participants_f'])
    df_events.reset_index(drop=True, inplace=True)

    # Add new columns that each contain the result of calculating the % of male and female participants
    df_events['Male'] = df_events['participants_m'] / df_events['participants']
    df_events['Female'] = df_events['participants_f'] / df_events['participants']

    # Sort the values by Type and Year
    df_events.sort_values(['type', 'year'], ascending=(True, True), inplace=True)
    # Create a new column that combines Location and Year to use as the x-axis
    df_events['xlabel'] = df_events['host'] + ' ' + df_events['year'].astype(str)

    # Create the stacked bar plot of the % for male and female
    df_events = df_events.loc[df_events['type'] == event_type]
    fig = px.bar(df_events,
                    x='xlabel',
                    y=['Male', 'Female'],
                    title=f'How has the ratio of female:male participants changed in {event_type} paralympics?',
                    labels={'xlabel': '', 'value': '', 'variable': ''},
                    template="simple_white",
                    color_discrete_map={'Male': 'blue', 'Female': 'green'}
                    )
    fig.update_xaxes(ticklen=0)
    fig.update_yaxes(tickformat=".0%")
    return fig


def scatter_geo():
    path = pathlib.Path(__file__).parent.parent.joinpath("data", "paralympics.db")
    # create database connection
    connection = sqlite3.connect(path)

    # define the sql query
    sql = '''
    SELECT event.year, host.host, host.latitude, host.longitude FROM event
    JOIN host_event ON event.event_id = host_event.event_id
    JOIN host on host_event.host_id = host.host_id
    '''

    # Use pandas read_sql to run a sql query and access the results as a DataFrame
    df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)

    # The lat and lon are stored as string but need to be floats for the scatter_geo
    df_locs['longitude'] = df_locs['longitude'].astype(float)
    df_locs['latitude'] = df_locs['latitude'].astype(float)

    # Adds a new column that concatenates the city and year e.g. Barcelona 2012
    df_locs['name'] = df_locs['host'] + ' ' + df_locs['year'].astype(str)

    # Create the figure
    fig = px.scatter_geo(df_locs,
                         lat=df_locs.latitude,
                         lon=df_locs.longitude,
                         hover_name=df_locs.name,
                         title="Where have the paralympics been held?",
                         )
    return fig


def create_card(host_year):
    """
    Generate a card for the event specified by host city name and year.

    Parameters:
        host_year: str  String with the host city name followed by a space then the year

    Returns:
        card: dash boostrap components card for the event
    """
    # Slice the string to get the year and host as separate values.
    # See https://www.w3schools.com/python/python_strings_slicing.asp
    # The last 4 digits are the year
    year = host_year[-4:] # add code in the brackets to get a slice of the string
    # Drop the last 5 digits (a space followed by the year) to the host city
    host = host_year[:-5] # add code in the brackets to get a slice of the string

    # Read the data into a DataFrame from the SQLite database
    path = pathlib.Path(__file__).parent.parent.joinpath("data", "paralympics.db")
    conn = sqlite3.connect(path)
    with conn:
        conn.execute("PRAGMA foreign_keys = ON")
        query = "SELECT * FROM event JOIN  host_event ON event.event_id = host_event.event_id JOIN host ON host_event.host_id = host.host_id WHERE event.year = ? AND host.host = ?;"
        event_df = pd.read_sql_query(query, conn, params=[year, host])

        # Variables for the card contents, the first is done for you as an example
        logo_path = f'logos/{year}_{host}.jpg'
        highlights = f'{event_df['highlights'].item()}'
        participants = f'{event_df['participants'].item()} athletes'
        events = f'{event_df['events'].item()} events'
        countries = f'{event_df['countries'].item()} participating teams'
        # sports = f'{event_df['sports'].item()} sports'

        card = dbc.Card([
            dbc.CardImg(src=dash.get_asset_url(logo_path), style={'max-width': '60px'}, top=True),
            dbc.CardBody([
                html.H4(host_year, className="card-title"),
                html.P(highlights, className="card-text", ),
                html.P(participants, className="card-text", ),
                html.P(events, className="card-text", ),
                html.P(countries, className="card-text", ),
            ]),
        ],
            style={"width": "18rem"},
        )
        return card
