import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

@app.callback(
    Output('data-storage', 'data'),
    [Input('dropdown', 'value'),
     State('data-storage', 'data')]
)
def update_filters(ddval, data):
    data = data or {'test': 'x'}
    data['gender'] = [ddval]
    return data