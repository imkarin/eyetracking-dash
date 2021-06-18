import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from plotly.shapeannotation import annotation_params_for_line, annotation_params_for_rect

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
def layout_perviewpoint(df, pathname, bgimg, width, height):
    # Filter DF based on pathname (welke viewpoint is het)
    layout = [
        dcc.Tabs(
            className='mb-5',
            children=
            [
                dcc.Tab(label='Eyetracker', children=tab_eyes(df, bgimg, width, height)),
                dcc.Tab(label='GSR', children=tab_gsr(df)),
                dcc.Tab(label='Head movement', children=tab_movement(df)),
                dcc.Tab(label='Data quality', children=tab_quality(df)),
        ])
    ]
    return layout

# Tab 1: Eyes
def tab_eyes(df, bgimg, width, height):
    # 3D Gaze
    fig_3dgaze = px.scatter_3d(df,
                             x='ET_Gaze3DX',
                             y='ET_Gaze3DY',
                             z='ET_Gaze3DZ',
                             title='Gaze X, Y and Z',
                             color='Resp name',
                             size_max=10,
                             opacity=0.4)

    # 2D Gaze
    fig_2dgazeinter = px.scatter(df,
                            x='Gaze X',
                            y='Gaze Y',
                            title='Gaze (average of left and right eye)',
                            color='Resp name',
                            opacity=0.4,
                            width=width,
                            height=height
                            )

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
                        color='Resp name',
                        title='Detected blinks',
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
        html.Section(       # Section: Gaze
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
                         x='Relative timestamp (s)',
                         color='Resp name',
                         title='GSR over time'
                         )

    # Tonic signal
    fig_tonic = px.line(df.sort_values('Timestamp'),
                         y='Tonic signal (microSiemens)',
                         x='Relative timestamp (s)',
                         color='Resp name',
                         title='Tonic signal over time'
                         )
    # Phasic signal
    fig_phasic = px.line(df.sort_values('Timestamp'),
                         y='Phasic signal (microSiemens)',
                         x='Relative timestamp (s)',
                         color='Resp name',
                         title='Phasic signal over time'
                         )
    
    # Peaks
    fig_peaks_detect = px.line(df.sort_values('Timestamp'),
                        y='Peak detected (binary)',
                         x='Relative timestamp (s)',
                        color='Resp name',
                        title='Peaks detected over time'
                        )

    fig_peaks_amp = px.line(df.sort_values('Timestamp'),
                        y='Peak amplitude (microSiemens)',
                         x='Relative timestamp (s)',
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
    # fig_gyrx = px.scatter(df,
    #             y='ET_GyroX',
    #             x='Relative timestamp (s)',
    #             color='Resp name',
    #             opacity=0.3).update_traces(marker_size=2)

    # fig_gyry = px.scatter(df,
    #             y='ET_GyroY',
    #             x='Relative timestamp (s)',
    #             color='Resp name',
    #             opacity=0.3).update_traces(marker_size=2)
                

    # fig_gyrz = px.scatter(df,
    #             y='ET_GyroZ',
    #             x='Relative timestamp (s)',
    #             color='Resp name',
    #             opacity=0.3).update_traces(marker_size=2)


    # fig_accx = px.scatter(df,
    #             y='ET_AccX',
    #             x='Relative timestamp (s)',
    #             color='Resp name',
    #             opacity=0.3).update_traces(marker_size=2)


    # fig_accy = px.scatter(df,
    #             y='ET_AccY',
    #             x='Relative timestamp (s)',
    #             color='Resp name',
    #             opacity=0.3).update_traces(marker_size=2)


    # fig_accz = px.scatter(df,
    #             y='ET_AccZ',
    #             x='Relative timestamp (s)',
    #             color='Resp name',
    #             opacity=0.3).update_traces(marker_size=2)

    
    fig_gyr = make_subplots(rows=1, cols=3)

    fig_gyr.add_trace(
        go.Scatter(x=df['Relative timestamp (s)'], y=df['ET_GyroX'], mode='markers', name='Gaze X', marker=dict(size=0.2)),
        row=1, col=1
    )

    fig_gyr.add_trace(
        go.Scatter(x=df['Relative timestamp (s)'], y=df['ET_GyroY'], mode='markers', name='Gaze Y', marker=dict(size=0.2)),
        row=1, col=2
    )

    fig_gyr.add_trace(
        go.Scatter(x=df['Relative timestamp (s)'], y=df['ET_GyroZ'], mode='markers', name='Gaze Z', marker=dict(size=0.2)),
        row=1, col=3
    )

    fig_gyr.update_layout(width=1100, height=450, title_text="Gyroscope X/Y/Z")


    fig_acc = make_subplots(rows=1, cols=3)

    fig_acc.add_trace(
        go.Scatter(x=df['Relative timestamp (s)'], y=df['ET_AccX'], mode='markers', name='Gaze X', marker=dict(size=0.2)),
        row=1, col=1
    )

    fig_acc.add_trace(
        go.Scatter(x=df['Relative timestamp (s)'], y=df['ET_AccY'], mode='markers', name='Gaze Y', marker=dict(size=0.2)),
        row=1, col=2
    )

    fig_acc.add_trace(
        go.Scatter(x=df['Relative timestamp (s)'], y=df['ET_AccZ'], mode='markers', name='Gaze Z', marker=dict(size=0.2)),
        row=1, col=3
    )

    fig_acc.update_layout(width=1100, height=450, title_text="Acceleration X/Y/Z")



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
                            width=12,
                            children=
                            [
                                dcc.Graph(figure=fig_gyr)
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    children= 
                    [
                        dbc.Col(
                            width=12,
                            children=
                            [
                                dcc.Graph(figure=fig_acc)
                            ]
                        ),
                    ]
                ),
            ]
        ),

    ]
    return tab_layout

# Tab 4: Data quality
def tab_quality(df):
    # info for the figures
    dist_max = df['ET_DistanceLeft'].max()

    # Distance scatter
    fig_dist = px.scatter(df,
                        y='ET_DistanceLeft',
                        x='Relative timestamp (s)',
                        opacity=0.3,
                        color='Resp name',
                        labels={
                            'ET_DistanceLeft': 'Distance',
                            'Relative timestamp (s)': 'Time (s)'
                        },
                        title='Distance').update_traces(marker_size=4)
    fig_dist.add_hline(y=900, line_width=1, line_color='red')
    fig_dist.add_hrect(y0=900, y1=dist_max+2000, fillcolor='red', opacity=0.15, line_width=0, 
                       annotation_text='90 centimeter threshold', annotation_position='bottom left')
    fig_dist.update_annotations(font_color='white')

    # Pupil diamater scatter
    fig_pupilscat = px.scatter(df,
                                x='Relative timestamp (s)',
                                y='ET_PupilLeft',
                                title='Pupil size',
                                color='Resp name',
                                opacity=0.2,
                                labels={
                                    'ET_PupilLeft': 'Pupil left (mm)',
                                    'Relative timestamp (s)': 'Time (s)'
                                },
                                ).update_traces(marker_size=4)
    fig_pupilscat.add_hrect(y0=4.7, y1=5.3, fillcolor='red', opacity=0.15, line_width=0, 
                            annotation_text='Outliers', annotation_position='bottom left')
    fig_pupilscat.update_annotations(font_color='white')

    # Validity scatter
    fig_val = px.scatter(df,
                        x='Relative timestamp (s)',
                        y='ET_ValidityLeftEye',
                        color='Resp name',
                        opacity=0.2,
                        title='Eye Validity (left)',
                        labels={
                            'ET_ValidityLeftEye': 'Validity',
                            'Relative timestamp (s)': 'Time (s)'
                        }
                        ).update_traces(marker_size=4)
    fig_val.add_hline(y=4, line_width=1, line_color='red', line_dash='dot',
                      annotation_text="iMotions: '4 = certainly invalid'", annotation_position='bottom left')
    fig_val.update_annotations(font_color='red', yshift=-2, xshift=2)

    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Distance to glasses'),
                html.P(children=
                    [
                        html.Span('Estimated distance between the Eyetracker and the eyes, measured by Tobii Glasses 2 (uninterpolated, left eye).'),
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
                                dcc.Graph(figure=fig_dist)
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