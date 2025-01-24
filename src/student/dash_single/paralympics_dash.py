import pathlib
# Imports for Dash and Dash.html and dcc
from dash import Dash, html, dcc
# Import Dash Bootstrap
import dash_bootstrap_components as dbc
# Add an import to import the line_chart function
from charts import line_chart

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case
# Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets,
           meta_tags=meta_tags,)

# Create the Plotly Express line chart object, e.g. to show number of sports
line_fig = line_chart("sports")

# Defining variables for each row
# Row 1
row_one = dbc.Row([
    dbc.Col([html.H1("Paralympics Data Analytics"),
             html.P("""Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                    Praesent congue luctus elit nec gravida.""")], width=12)
])

# Row 2
row_two = dbc.Row([
    dbc.Col(children=[dbc.Select(options=[
        {"label": "Events", "value": "events"},  # The value is in the format of the column heading in the data
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ], value="events",  # The default selection
    id="dropdown-input",  # id uniquely identifies the element, will be needed later for callbacks
    )], width=4),

    dbc.Col(children=[html.Div([
        dbc.Label("Select the Paralympic Games type"),
        dbc.Checklist(
            options=[
                {"label": "Summer", "value": "summer"},
                {"label": "Winter", "value": "winter"},
            ],
            value=["summer"],  # Values is a list as you can select 1 AND 2
            id="checklist-input"),
        ])], width={"size": 4, "offset": 2}),
    # 2 'empty' columns between this and the previous column
])

# Row 3
row_three = dbc.Row([
    dbc.Col([html.Img(src=app.get_asset_url('line-chart-placeholder.png'),
             className="img-fluid")], width=6),
    dbc.Col([html.Img(src=app.get_asset_url('bar-chart-placeholder.png'),
             className="img-fluid")], width=6),
])

# Row 4
row_four = dbc.Row([
    dbc.Col([html.Img(src=app.get_asset_url('line-chart-placeholder.png'),
             className="img-fluid")], width=8),


    dbc.Col([dbc.Card([
        dbc.CardImg(src=app.get_asset_url("logos/2022_Beijing.jpg"), top=True),
        dbc.CardBody([
            html.H4("Beijing 2022", className="card-title"),
            html.P("Number of athletes: XX", className="card-text", ),
            html.P("Number of events: XX", className="card-text", ),
            html.P("Number of countries: XX", className="card-text", ),
            html.P("Number of sports: XX", className="card-text", ),
            ]),
    ], style={"width": "18rem"},)], width=4),
])

# Wrap the layout in a Bootstrap container
app.layout = dbc.Container([
    # The layout will go here
    row_one,
    row_two,
    row_three,
    row_four,
    # Add the chart to the layout
    dcc.Graph(id="line-chart", figure=line_fig)
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)
