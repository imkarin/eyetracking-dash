import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

from app import app

# Layout of the page: Home
# This function generates the html elements
# with updated plots that match the filters (respondents)

def layout_home(df):
    # figures
    fig = px.scatter(x=df['Resp rec datetime'].unique(),
                     y=df['Resp name'].unique())
    
    # page layout
    layout = [
        dbc.Row(
            children=
            [
                dbc.Col(
                    dcc.Graph(figure=fig)
                )
            ]
        )
    ]

    return layout