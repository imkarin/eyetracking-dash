from numpy import diff
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
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
    # global dff 
    # dff = df.copy()

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
        html.Div(id='tabs-content')
    ])
    return layout

# ROUTING TABS: The clicked tab determines the content shown in the tabs-content Div
# @app.callback(Output('tabs-content', 'children'),
#               Input('tabs-nav', 'value'))
# def show_tabcontent(tab):
#     if tab == 'tab-eyetracker':
#         return tab_eyes(dff)

#     elif tab == 'tab-gsr':
#         return tab_gsr(dff)
    
#     elif tab == 'tab-movement':
#         return tab_quality(dff)
        
#     elif tab == 'tab-quality':
#         return tab_movement(dff)


# Tab 1: Eyes
def tab_eyes(df):
    # Gaze 2D/3D
    fig_3dgaze = px.scatter_3d(x=df['ET_Gaze3DX'],
                             y=df['ET_Gaze3DY'],
                             z=df['ET_Gaze3DZ'],
                             title='Gaze X, Y and Z',
                             size_max=10,
                             opacity=0.5)
                    
    fig_2dgazeinter = px.scatter(df,
                            x='Interpolated Gaze X',
                            y='Interpolated Gaze Y',
                            title='Interpolated Gaze')

    # Pupil diameter
    fig_pupilscat = px.scatter(df,
                        x='ET_PupilLeft',
                        y='ET_PupilRight',
                        title='Pupil size',
                        labels={
                            "ET_PupilLeft": "Pupil left (mm)",
                            "ET_PupilRight": "Pupil right (mm)"})
    
    # Blink
    fig_blink = px.histogram(df,
                        x='Blink detected (binary)',
                        title='Detected blinks',
                        nbins=2)
    
    # Fixation
    fig_fixationxy = px.scatter(df[df['Fixation X'].notna()],
                            x='Fixation X',
                            y='Fixation Y',
                            color='Fixation Dispersion',
                            size='Fixation Duration',
                            opacity=.2,
                            title='Fixation coordinates, dispersion and duration')

    # Saccade
    #...

    # fig_pupilsbar = px.bar(df,
    #                     x='ET_PupilLeft',
    #                     title='Pupil size',
    #                     labels={
    #                         "ET_PupilLeft": "Pupil left (mm)",})

    # fig_gazevelacc = px.scatter(df,
    #                         x='Gaze Velocity',
    #                         y='Gaze Acceleration',
    #                         title='Gaze Velocity and Acceleration')



    # fig_fixationstartend = px.scatter(df,
    #                         x='Fixation Start',
    #                         y='Fixation End',
    #                         title='Fixation Start and End')

    # fig_velacc = px.scatter(df,
    #                         x='Saccade Peak Velocity',
    #                         y='Saccade Peak Acceleration',
    #                         title='Peak Velocity & Peak Acceleration')

    # fig_accdel = px.scatter(df,
    #                         x='Saccade Peak Deceleration',
    #                         y='Saccade Peak Acceleration',
    #                         title='Peak Deceleration & Peak Acceleration')

    # fig_durdir = px.scatter(df,
    #                         x='Saccade Direction',
    #                         y='Saccade Duration',
    #                         title='Duration & Direction')
                    
    # fig_ampvel = px.scatter(df,
    #                         x='Saccade Amplitude',
    #                         y='Saccade Peak Velocity',
    #                         title='Amplitude & Peak Velocity')



    # the layout
    tab_layout = [
        html.Section(           # Section: Gaze points
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

        html.Section(           # Section: blink/pupil
            className='mt-5',
            children=
            [
                html.H4('Pupil diameter & blinks'),
                html.P(f'Information'),
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
                html.P(f'Information'),
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
                        # dbc.Col(
                        #     width=6,
                        #     children=
                        #     [
                        #         dcc.Graph(figure=fig_fixationstartend)
                        #     ]
                        # ),
                    ]
                ),
            ]
        ),

        html.Section(           # Section: Saccade
            className='mt-5',
            children=
            [
                html.H4('Saccade'),
                html.P(f'Information'),
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
                    ]
                ),
            ]
        )
    ]
    return tab_layout

# Tab 2: GSR
def tab_gsr(df):
    fig_tonic = px.line(df,
                y='Tonic signal (microSiemens)')
    
    fig_phasic = px.line(df,
                y='Phasic signal (microSiemens)')

    fig_gsrraw = px.line(df,
                y='GSR RAW')

    fig_gsrinter = px.line(df,
                y='GSR Interpolated (microSiemens)(GSRPEAK=IsPeak)(GSRONSET=GsrOnset)(GSROFFSET=GsrOffset)')

    fig_intertonic = px.scatter(df,
                x='GSR Interpolated (microSiemens)(GSRPEAK=IsPeak)(GSRONSET=GsrOnset)(GSROFFSET=GsrOffset)',
                y='Tonic signal (microSiemens)')

    fig_interphasic = px.scatter(df,
                x='GSR Interpolated (microSiemens)(GSRPEAK=IsPeak)(GSRONSET=GsrOnset)(GSROFFSET=GsrOffset)',
                y='Phasic signal (microSiemens)')


    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Header'),
                html.P(f'Information'),
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
                ),
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
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_gsrinter)
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_intertonic)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_interphasic)
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
    return tab_layout

# Tab 3: Movement
def tab_movement(df):
    fig_gyrx = px.line(df,
                y='ET_GyroX')

    fig_gyry = px.line(df,
                y='ET_GyroY')

    fig_gyrz = px.line(df,
                y='ET_GyroZ')

    fig_accx = px.line(df,
                y='ET_AccX')

    fig_accy = px.line(df,
                y='ET_AccY')

    fig_accz = px.line(df,
                y='ET_AccZ')



    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Header'),
                html.P(f'Information'),
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

    fig_eye3d = px.scatter_3d(df,
                x='ET_DistanceLeft',
                y='ET_DistanceRight',
                z='ET_Distance3D')

    fig_int = px.line(df,
                y='Interpolated Distance',
                title='Interpolated Distance')

    fig_pupilscat = px.scatter(df,
                        x='ET_PupilLeft',
                        y='ET_PupilRight',
                        title='Pupil size',
                        labels={
                            "ET_PupilLeft": "Pupil left (mm)",
                            "ET_PupilRight": "Pupil right (mm)"})

    fig_val = px.line(df,
                x='ET_ValidityLeftEye',
                y='ET_ValidityRightEye',
                title='Eye Validity')

    # fig_xbar = px.bar(df,
    #             x='ET_GazeDirectionLeftX',
    #             y='ET_GazeDirectionRightX')

    # fig_xcolumn = px.line(df,
    #             x='ET_GazeDirectionLeftX',
    #             y='ET_GazeDirectionRightX')

    # fig_xline = px.line(df,
    #             x='ET_GazeDirectionLeftX',
    #             y='ET_GazeDirectionRightX')

    # fig_ybar = px.bar(df,
    #             x='ET_GazeDirectionLeftY',
    #             y='ET_GazeDirectionRightY')

    # fig_ycolumn = px.line(df,
    #             x='ET_GazeDirectionLeftY',
    #             y='ET_GazeDirectionRightY')

    # fig_yline = px.line(df,
    #             x='ET_GazeDirectionLeftY',
    #             y='ET_GazeDirectionRightY')

    # fig_zbar = px.bar(df,
    #             x='ET_GazeDirectionLeftZ',
    #             y='ET_GazeDirectionRightZ')

    # fig_zcolumn = px.line(df,
    #             x='ET_GazeDirectionLeftZ',
    #             y='ET_GazeDirectionRightZ')

    # fig_zline = px.line(df,
    #             x='ET_GazeDirectionLeftZ',
    #             y='ET_GazeDirectionRightZ')

    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Header'),
                html.P(f'Information'),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_eye3d)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_int)
                            ]
                        ),
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