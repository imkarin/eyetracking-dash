import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

from app import app

# Layout of the page: Data per viewpoint
# This function generates the html elements
# with updated plots that match the filters (respondents)

def layout_perviewpoint(df):
    # figures
    # fig = 
    
    # page layout
    layout = [
        dbc.Row(
            children=
            [
                dbc.Col(
                    dcc.Graph()
                )
            ]
        )
    ]

    return layout