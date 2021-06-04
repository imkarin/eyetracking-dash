import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

from app import app

# Layout of the page: DATA PER VIEWPOINT (1)
# The functions in this file generate the HTML elements with updated plots

# Functions generate:
# - Tab 1: Eyes
# - Tab 2: GSR
# - Tab 3: Movement
# - Tab 4: Data quality
# - layout_home combines all the tabs into 1 page layout

# Combined layout:
def layout_perviewpoint(df):
    layout = [
        dcc.Tabs(
            className='mb-5',
            children=
            [
                dcc.Tab(label='Eyetracker', children=tab_eyes(df)),
                dcc.Tab(label='GSR', children=tab_gsr(df)),
                dcc.Tab(label='Head movement', children=tab_movement(df)),
                dcc.Tab(label='Data quality', children=tab_quality(df)),
        ])
    ]
    return layout

# Tab 1: Eyes
def tab_eyes(df):
    # figures/variables here...

    # the layout
    tab_layout = [
        # html elements/plots (containing the figs) here
    ]
    return tab_layout

# Tab 2: GSR
def tab_gsr(df):
    tab_layout = [
        # html elements/plots here
    ]
    return tab_layout

# Tab 3: Movement
def tab_movement(df):
    tab_layout = [
        # html elements/plots here
    ]
    return tab_layout

# Tab 4: Data quality
def tab_quality(df):
    tab_layout = [
        # html elements/plots here
    ]
    return tab_layout