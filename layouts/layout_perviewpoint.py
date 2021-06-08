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
def layout_perviewpoint(df, pathname, bgimg):
    # Filter DF based on pathname (welke viewpoint is het)
    layout = [
        dcc.Tabs(
            className='mb-5',
            children=
            [
                dcc.Tab(label='Eyetracker', children=tab_eyes(df, bgimg)),
                dcc.Tab(label='GSR', children=tab_gsr(df)),
                dcc.Tab(label='Head movement', children=tab_movement(df)),
                dcc.Tab(label='Data quality', children=tab_quality(df)),
        ])
    ]
    return layout

# Tab 1: Eyes
def tab_eyes(df, bgimg):
    fig_3dgaze = px.scatter_3d(x=df['ET_Gaze3DX'],
                             y=df['ET_Gaze3DY'],
                             z=df['ET_Gaze3DZ'],
                             title='Gaze X, Y and Z',
                             size_max=10,
                             opacity=0.4)

    fig_2dgazeinter = px.scatter(df,
                            x='Interpolated Gaze X',
                            y='Interpolated Gaze Y',
                            title='Interpolated Gaze',
                            opacity=0.4)

    fig_2dgazeinter.update_layout(
                images= [dict(
                    source='data:image/png;base64,{}'.format(bgimg.decode()),
                    xref="paper", yref="paper",
                    sizing='stretch',
                    opacity=1,
                    x=0, y=1,
                    sizex=1, sizey=1,
                    xanchor="left",
                    yanchor="top",
                    #sizing="stretch",
                    layer="below")])

    fig_pupilscat = px.scatter(df,
                        x='ET_PupilLeft',
                        y='ET_PupilRight',
                        title='Pupil size',
                        opacity=0.4,
                        labels={
                            "ET_PupilLeft": "Pupil left (mm)",
                            "ET_PupilRight": "Pupil right (mm)"})

    fig_blink = px.histogram(df,
                        x='Blink detected (binary)',
                        title='Detected blinks',
                        nbins=2)


    # the layout
    tab_layout = [
        html.Section(       # Section: Gaze
            className='mt-5',
            children=
            [
                html.H4('Gaze points'),
                html.P(f'Information'),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_3dgaze)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_2dgazeinter)
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Section(           # Section: Pupil & blink
            className='mt-5',
            children=
            [
                html.H4('Pupil diameter & blinks'),
                html.P('Information'),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_pupilscat)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_blink)
                            ]
                        ),
                    ]
                ),
            ]
        ),
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