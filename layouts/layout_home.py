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
    # figures
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

    # table with stats
    table_header = [
        html.Thead(html.Tr([html.Th("Viewpoint"), 
                            html.Th("Blink rate"),
                            html.Th("GSR peaks"),
                            html.Th("GSR raw"),
                            html.Th("Fixations amount"),
                            html.Th("Fixations duration"),
                            html.Th("Fixations dispersion"),
                            html.Th("Saccades amount"),
                            html.Th("Saccades duration"),
                            html.Th("Saccades amplitude"),
                            ]))
    ]

    row1 = html.Tr([html.Td("1"), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value')])
    row2 = html.Tr([html.Td("2"), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value')])
    row3 = html.Tr([html.Td("3"), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value')])
    row4 = html.Tr([html.Td("4"), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value')])
    row5 = html.Tr([html.Td("5"), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value'), html.Td('Value')])

    table_body = [html.Tbody([row1, row2, row3, row4, row5])]
    stats_table = dbc.Table(table_header + table_body, bordered=True)

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
                            width=12,
                            children=
                            [
                                stats_table
                            ]
                        ),
                    ]
                ),
            ]
        ),  # End Section 'stats tables'

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