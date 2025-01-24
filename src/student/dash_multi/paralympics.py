import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=meta_tags, use_pages=True)

# From https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Event Details", href=dash.page_registry['pages.events']['path'])),
        dbc.NavItem(dbc.NavLink("Charts", href=dash.page_registry['pages.charts']['path'])),
    ],
    brand="Paralympics Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)

app.layout = dbc.Container([
    # Nav bar
    navbar,
    # Area where the page content is displayed
    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=True)
