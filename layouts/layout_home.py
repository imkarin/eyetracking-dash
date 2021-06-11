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

    # other info
    date = df['Resp rec datetime'].dt.date.mode()[0]
    amt_resp = df['Resp name'].nunique()

    # table with viewpoint stats
    stats_cols = ['Timestamp', 'Resp name',
                  'Blink detected (binary)', 'GSR Raw (microSiemens)', 'Peak detected (binary)',
                  'Fixation Index', 'Fixation Duration', 'Fixation Dispersion',
                  'Saccade Index', 'Saccade Duration', 'Saccade Amplitude']
    vp_cols = ([col for col in df.columns if all(vpa in col for vpa in ['Viewpoint', 'active'])])
    vpdf = df[stats_cols + vp_cols].copy()
    
    def get_vp_stats():
        vp_stats_default = {'Viewpoint' : '-',
                            'Blinkrate' : '-', 
                            'GSR peaks' : '-', 
                            'GSR raw' : '-', 
                            'Fixations amount' : '-', 
                            'Fixations duration' : '-',
                            'Fixations dispersion' : '-', 
                            'Saccades amount' : '-', 
                            'Saccades duration' : '-', 
                            'Saccades amplitude': '-'}
        vps_data = []
        
        for i, vp_col in enumerate(sorted(vp_cols)):
            # get the df where vp = active
            vp = vpdf[vpdf[vp_col] == 1]
            vp_stats = vp_stats_default.copy()
            vp_stats['Viewpoint'] = i + 1

            # replace vp_stats with actual stats
            if len(vp) > 0:
                blinkrate = round(vp['Blink detected (binary)'].mean(), 4)
                gsr_peaks = len(vp[vp['Peak detected (binary)'] == 1]) / amt_resp

                vp_stats['Blinkrate'] = blinkrate
                vp_stats['GSR peaks'] = gsr_peaks
                # vp_stats['GSR raw'] = 
                # vp_stats['Fixations amount'] = 
                # vp_stats['Fixations duration'] = 
                # vp_stats['Fixations dispersion'] = 
                # vp_stats['Saccades amount'] = 
                # vp_stats['Saccades duration'] = 
                # vp_stats['Saccades amplitude'] = 
            
            vps_data.append(vp_stats)


        return vps_data

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
    # Generate table cells with vp stats
    table_rows = [
        html.Tr([html.Td(vp_stats['Viewpoint']), 
                 html.Td(vp_stats['Blinkrate']), 
                 html.Td(vp_stats['GSR peaks']), 
                 html.Td(vp_stats['GSR raw']), 
                 html.Td(vp_stats['Fixations amount']), 
                 html.Td(vp_stats['Fixations duration']), 
                 html.Td(vp_stats['Fixations dispersion']), 
                 html.Td(vp_stats['Saccades amount']), 
                 html.Td(vp_stats['Saccades duration']), 
                 html.Td(vp_stats['Saccades amplitude'])])
        for vp_stats in get_vp_stats()
    ]

    table_body = [html.Tbody(table_rows)]
    vpstats_table = dbc.Table(table_header + table_body, bordered=True)

    # page layout
    layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Viewpoint stats'),
                html.P(f'Statistic on the viewpoints from the recording sessions in Amsterdam, on {date}. You have selected {amt_resp} respondents.'),
                dbc.Row(
                    children=
                    [
                        dbc.Col(   # recording start time
                            width=12,
                            children=
                            [
                                vpstats_table
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