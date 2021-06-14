from numpy import diff
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import base64

from app import app

# Layout of the page: DATA FULL ROUTE
# The functions in this file generate the HTML elements with updated plots

# Functions generate:
# - Tab 1: Eyes
# - Tab 2: GSR
# - Tab 3: Movement
# - Tab 4: Data quality
# - layout_home combines all the tabs into 1 page layout

# Combined layout:
def layout_fullroute(df):
    layout = html.Div([
        dcc.Tabs(
            id='tabs-nav',
            value='tab-eyetracker',
            className='mb-5',
            children=
            [
                dcc.Tab(label='Eyetracker', value='tab-eyetracker', children=tab_eyes(df)),
                dcc.Tab(label='GSR', value='tab-gsr', children=tab_gsr(df)),
                dcc.Tab(label='Head movement', value='tab-movement', children=tab_movement(df)),
                dcc.Tab(label='Data quality', value='tab-quality', children=tab_quality(df)),
        ]),
        # html.Div(id='tabs-content')
    ])
    return layout


# Tab 1: Eyes
def tab_eyes(df):
    # Gaze 2D/3D
    fig_3dgaze = px.scatter_3d(df,
                            x='ET_Gaze3DX',
                             y='ET_Gaze3DY',
                             z='ET_Gaze3DZ',
                             title='Gaze 3D',
                             color='Resp name',
                             size_max=10,
                             opacity=0.2)
                    
    fig_2dgazeinter = px.scatter(df,
                            x='Gaze X',
                            y='Gaze Y',
                            opacity=0.2,
                            color='Resp name',
                            title='Gaze (average of left and right eye)')

    # Pupil diameter
    fig_pupilscat = px.scatter(df,
                        x='ET_PupilLeft',
                        y='ET_PupilRight',
                        title='Pupil size',
                        color='Resp name',
                        opacity=.1,
                        labels={
                            "ET_PupilLeft": "Pupil left (mm)",
                            "ET_PupilRight": "Pupil right (mm)"})
    
    # Blink
    fig_blink = px.histogram(df,
                        x='Blink detected (binary)',
                        title='Detected blinks',
                        color='Resp name',
                        nbins=2)
    
    # Fixation
    fig_fixationxy = px.scatter(df[df['Fixation X'].notna()],
                            x='Fixation X',
                            y='Fixation Y',
                            color='Fixation Dispersion',
                            size='Fixation Duration',
                            opacity=.3,
                            title='Fixation coordinates, dispersion and duration')

    # Saccade
    # ...

    # the layout
    tab_layout = [
        html.Section(           # Section: Gaze points
            className='mt-5',
            children=
            [
                html.H4('Gaze points'),
                html.P(children=
                [
                    html.Span('Gaze points of the respondents.'),
                    html.Br(),
                    html.Span('''2D points: coordinates (X, Y) of the gaze point, relative to top left corner of the screen,
                    average of left and right eye, uninterpolated).'''),
                    html.Br(),
                    html.Span('''3D points: coordinates (X, Y, Z) of the gaze point, relative to position of eyetracker's scene camera.'''),
                ]),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_2dgazeinter)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_3dgaze)
                            ]
                        ),
                    ]
                ),
            ]
        ),

        html.Section(           # Section: blink/pupil
            className='mt-5',
            children=
            [
                html.H4('Pupil diameter & blinks'),
                html.P(children=
                [
                    html.Span('Pupil diameter and blink detection.'),
                    html.Br(),
                    html.Span('''Pupil diameter: diameter of the left (x-axis) and right (y-axis) pupil.'''),
                    html.Br(),
                    html.Span('''Blink detection: binary representation of blinks (y-axis) over time (x-axis), where 1 = blink, 0 = no blink.'''),
                ]),
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

        html.Section(           # Section: Fixations
            className='mt-5',
            children=
            [
                html.H4('Fixations'),
                html.P(children=
                [
                    html.Span('Fixations X and Y coordinates plotted against each other, where size = fixation duration and color = fixation dispersion.'),
                ]),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_fixationxy)
                            ]
                        ),
                        # Add fixation plots...
                    ]
                ),
            ]
        ),
    ]
    return tab_layout


# Tab 2: GSR
def tab_gsr(df):
    # GSR Raw
    fig_gsrraw = px.line(df.sort_values('Timestamp'),
                         y='GSR Raw (microSiemens)',
                         x='Timestamp (s)',
                         color='Resp name',
                         title='GSR over time'
                         )

    # Tonic signal
    fig_tonic = px.line(df.sort_values('Timestamp'),
                         y='Tonic signal (microSiemens)',
                         x='Timestamp (s)',
                         color='Resp name',
                         title='Tonic signal over time'
                         )
    # Phasic signal
    fig_phasic = px.line(df.sort_values('Timestamp'),
                         y='Phasic signal (microSiemens)',
                         x='Timestamp (s)',
                         color='Resp name',
                         title='Phasic signal over time'
                         )
    
    # Peaks
    fig_peaks_detect = px.line(df.sort_values('Timestamp'),
                        y='Peak detected (binary)',
                         x='Timestamp (s)',
                        color='Resp name',
                        title='Peaks detected over time'
                        )

    fig_peaks_amp = px.line(df.sort_values('Timestamp'),
                        y='Peak amplitude (microSiemens)',
                         x='Timestamp (s)',
                        color='Resp name',
                        title='Peaks detected over time'
                        )

    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('GSR Raw'),
                html.P(children=
                [
                    html.Span('Processed and imported data GSR peaks.'),
                    html.Br(),
                    html.Span('''Raw measurements of GSR signal'''),
                ]),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_gsrraw)
                            ]
                        ),
                    ]
                ),
            ]
        ),

        html.Section(
            children=
            [
                html.H4('Tonic & Phasic signal'),
                html.P(children=
                [
                    html.Span('Tonic and Phasic signal (y-axis) over time in seconds (x-axis).'),
                ]),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_tonic)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_phasic)
                            ]
                        ),
                    ]
                )
            ]
        ),

        html.Section(
            children=
            [
                html.H4('GSR Peaks'),
                html.P(children=
                [
                    html.Span('Peaks detected: binary representation of GSR peaks (y-axis) over time (x-axis), where 1 = peak and 0 = no peak.'),
                    html.Br(),
                    html.Span('Peaks amplitude: amplitude of GSR peaks (y-axis) over time (x-axis).'),
                ]),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_peaks_detect)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_peaks_amp)
                            ]
                        ),
                    ]
                )
            ]
        )
    ]


    return tab_layout

# Tab 3: Movement
def tab_movement(df):
    fig_gyrx = px.scatter(df,
                y='ET_GyroX',
                x='Timestamp (s)',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)

    fig_gyry = px.scatter(df,
                y='ET_GyroY',
                x='Timestamp (s)',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)
                

    fig_gyrz = px.scatter(df,
                y='ET_GyroZ',
                x='Timestamp (s)',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)


    fig_accx = px.scatter(df,
                y='ET_AccX',
                x='Timestamp (s)',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)


    fig_accy = px.scatter(df,
                y='ET_AccY',
                x='Timestamp (s)',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)


    fig_accz = px.scatter(df,
                y='ET_AccZ',
                x='Timestamp (s)',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)




    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Head movement'),
                html.P(children=
                [
                    html.Span('Movement of the head measured by Tobii Glasses 2.'),
                    html.Br(),
                    html.Span('''Gyroscope: Rotation of the glasses along the X, Y an Z axis over time.'''),
                    html.Br(),
                    html.Span('''Accelerometer: Motion along the X, Y and Z axis over time.'''),
                ]),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_gyrx)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_gyry)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_gyrz)
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_accx)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_accy)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_accz)
                            ]
                        )
                    ]
                ),
            ]
        ),

    ]
    return tab_layout

# Tab 4: Data quality
def tab_quality(df):
    fig_int = px.scatter(df,
                        y='ET_DistanceLeft',
                        x='Timestamp (s)',
                        opacity=0.3,
                        color='Resp name',
                        title='Distance')

    fig_pupilscat = px.scatter(df,
                                x='Timestamp (s)',
                                y='ET_PupilLeft',
                                title='Pupil size',
                                color='Resp name',
                                opacity=0.3,
                                )

    fig_val = px.scatter(df,
                        x='Timestamp (s)',
                        y='ET_ValidityLeftEye',
                        opacity=0.3,
                        color='Resp name',
                        title='Eye Validity (left)')

    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.P('Insights in the validity & quality of the measured data.'),
                html.Br(),
                html.H4('Distance'),
                html.P(children=
                    [
                        html.Span('Estimated distance between the Eyetracker glasses and the eyes, measured by Tobii Glasses 2 (uninterpolated, left eye).'),
                        html.Br(),
                        html.Span('Distance on the y-axis, timestamp on the x-axis.'),
                    ]
                ),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=12,
                            children=
                            [
                                dcc.Graph(figure=fig_int)
                            ]
                        ),
                    ]
                ),
            ]
        ),

        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Pupil size & Data validity'),
                html.P(children=
                    [
                        html.Span('''Pupil diameter: diameter of the left (x-axis) and right (y-axis) pupil.'''),
                        html.Br(),
                        html.Span('Validity: Level of certainty that the eyetracker has recorded valid data for the left eye (y-axis) over time (x-axis), where 0 = certainly valid and 5 = certainly invalid.'),
                    ]
                ),
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
                                dcc.Graph(figure=fig_val)
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
    return tab_layout