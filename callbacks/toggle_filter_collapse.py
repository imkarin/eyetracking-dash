import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

# Filter collapse callback
@app.callback(
    Output("filter-collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("filter-collapse", "is_open")],
)
def toggle_filter_collapse(n, is_open):
    if n:
        return not is_open
    return is_open