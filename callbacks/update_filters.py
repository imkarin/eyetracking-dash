import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

@app.callback(
    Output('data-storage', 'data'),
    [Input('filter-gender-checklist', 'value'),
     Input('filter-age-slider', 'value'),
     Input('filter-timebegin-input', 'value'),
     Input('filter-timeend-input', 'value'),
     State('data-storage', 'data')]
)
def update_filters(gender, age, timebegin, timeend, data):
    data = data or {'test': 'x'}
    data['gender'] = gender
    data['age'] = list(range(age[0], age[1]+1))
    data['time'] = [timebegin, timeend]
    print(data['time'])
    print(data['age'])
    return data