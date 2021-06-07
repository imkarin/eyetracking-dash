import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

@app.callback(
    Output('data-storage', 'data'),
    [Input('filter-respname', 'value'),
    #  Input('filter-gender-checklist', 'value'),
    #  Input('filter-age-slider', 'value'),
    #  Input('filter-timebegin-input', 'value'),
    #  Input('filter-timeend-input', 'value'),
     State('data-storage', 'data')]
)
def update_filters(respname, data):
    data = data or {'test': 'x'}
    data['respname'] = respname
    # Old filters:
    # data['gender'] = gender                      # list of genders
    # data['age'] = list(range(age[0], age[1]+1))  # list of ages
    # data['time'] = [timebegin, timeend]          # list of strings representing time
    #                                              # will be processed in index.py
    #                                              # because dcc.Store can't hold datetime types

    return data