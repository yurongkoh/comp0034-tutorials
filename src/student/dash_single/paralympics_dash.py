import pathlib
# Imports for Dash and Dash.html and dcc
from dash import Dash, html, dcc, Input, Output
# Import Dash Bootstrap
import dash_bootstrap_components as dbc
from student.dash_single.charts import line_chart, bar_gender, scatter_geo, create_card
import os
from selenium.webdriver.chrome.options import Options


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

# Create the Plotly Express bar chart object
bar_fig = bar_gender("summer")  # Insert 'winter' or 'summer'

# Create the scatter map
map = scatter_geo()

# Create a card variable
card = create_card("Barcelona 1992")

# Defining variables for each row
# Row 1
row_one = dbc.Row([
    dbc.Col([html.H1("Paralympics Dashboard"),
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
    dbc.Col(children=[dcc.Graph(id="line-chart", figure=line_fig), ], width=6),
    dbc.Col(children=[], id='bar-div', width=6),
], align="start")

# Row 4
row_four = dbc.Row([
    dbc.Col(children=[dcc.Graph(id='map', figure=map)], width=8),
    dbc.Col(children=[card], id='card', width=4),
], align="start")

# Wrap the layout in a Bootstrap container
app.layout = dbc.Container([
    # The layout will go here
    row_one,
    row_two,
    row_three,
    row_four,
    # # Add the line chart to the layout
    # dcc.Graph(id="line-chart", figure=line_fig),
    # # Add the bar chart to the layout
    # dcc.Graph(id="bar-chart", figure=bar_fig),
    # dcc.Graph(id="geo-scatter", figure=map)
])


@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    Input(component_id='dropdown-input', component_property='value')
)
def update_line_chart(feature):
    figure = line_chart(feature)
    return figure


@app.callback(
    Output(component_id='bar-div', component_property='children'),
    Input(component_id='checklist-input', component_property='value')
)
def update_bar_chart(selected_values):
    """ Updates the bar chart based on the checklist selection.
     Creates one chart for each of the selected values.
     """
    figures = []
    # Iterate the list of values from the checkbox component
    for value in selected_values:
        fig = bar_gender(value)
        # Assign id to be used to identify the charts
        id = f"bar-chart-{value}"
        element = dcc.Graph(figure=fig, id=id)
        figures.append(element)
    return figures


@app.callback(
    Output('card', 'children'),
    Input('map', 'hoverData'),
)
def display_card(hover_data):
    if not hover_data:
        return
    text = hover_data['points'][0]['hovertext']
    if text is not None:
        return create_card(text)


def pytest_setup_options():
    """pytest extra command line arguments for running chrome driver

     For GitHub Actions or similar container you need to run it headless.
     When writing the tests and running locally it may be useful to
     see the browser and so you need to see the browser.
    """
    options = Options()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    return options

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)
