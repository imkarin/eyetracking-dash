import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

from app import app

# Layout of the page: HOME
# The functions in this file generate the HTML elements with updated plots
# This page has no tabs.

# Combined layout:
def layout_home(df):
    fig_rectime = px.scatter(x=df['Resp rec datetime'].unique(),
                             y=df['Resp name'].unique(),
                             title='Starttime recording')
    
    genders = []    
    for resp in df['Resp name'].unique():
        genders.append(df[df['Resp name'] == resp]['Resp gender'].iloc[0])

    fig_gender = px.pie(genders, names=genders, title='Genders')

    ages = []
    for resp in df['Resp name'].unique():
        ages.append(df[df['Resp name'] == resp]['Resp age'].iloc[0])

    fig_age = px.histogram(ages, title='Ages')


    # other info
    date = df['Resp rec datetime'].dt.date.mode()[0]

    # page layout
    layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Recording session'),
                html.P(f'Information about the recording sessions in Amsterdam, on {date}.'),
                dbc.Row(
                    children=
                    [
                        dbc.Col(   # recording start time
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_rectime)
                            ]
                        ),
                        # dbc.Col(    # recording start time
                        #     width=6,
                        #     children=
                        #     [
                        #         dcc.Graph(figure=fig_rectime)
                        #     ]
                        # )
                    ]
                ),
            ]
        ),  # End Section 'recording session'

        html.Section(
            className='',
            children=
            [
                html.H4("Respondents"),
                html.P('Information about the respondents of the recording sessions'),
                dbc.Row(
                    children=
                    [
                        dbc.Col(    # gender pie
                            width=6,
                            children=
                            [   
                                dcc.Graph(figure=fig_gender)
                            ]
                        ),
                        dbc.Col(    # age counts
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_age)
                            ]
                        ),
                    ]
                )
            ]
        )   # End Section 'respondent info'
    ]
    return layout