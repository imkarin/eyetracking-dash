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
    fig_3dgaze = px.scatter_3d(x=df['ET_Gaze3DX'],
                             y=df['ET_Gaze3DY'],
                             z=df['ET_Gaze3DZ'],
                             title='Gaze X, Y and Z',
                             size_max=10,
                             opacity=0.5)

    fig_pupilscat = px.scatter(df,
                        x='ET_PupilLeft',
                        y='ET_PupilRight',
                        title='Pupil size',
                        labels={
                            "ET_PupilLeft": "Pupil left (mm)",
                            "ET_PupilRight": "Pupil right (mm)"})
    
    fig_pupilsbar = px.bar(df,
                        x='ET_PupilLeft',
                        title='Pupil size',
                        labels={
                            "ET_PupilLeft": "Pupil left (mm)",})
                    
    fig_2dgazeinter = px.scatter(df,
                            x='Interpolated Gaze X',
                            y='Interpolated Gaze Y',
                            title='Interpolated Gaze')

    #set a local image as a background
    image_filename = 'assets\img\Viewport_Panorama-1.jpg'
    plotly_logo = base64.b64encode(open(image_filename, 'rb').read())

    fig_2dgazeinter.update_layout(
                images= [dict(
                    source='data:image/png;base64,{}'.format(plotly_logo.decode()),
                    xref="paper", yref="paper",
                    sizing='stretch',
                    opacity=1,
                    x=0, y=1,
                    sizex=1, sizey=1,
                    xanchor="left",
                    yanchor="top",
                    #sizing="stretch",
                    layer="below")])

    fig_gazevelacc = px.scatter(df,
                            x='Gaze Velocity',
                            y='Gaze Acceleration',
                            title='Gaze Velocity and Acceleration')

    fig_fixationxy = px.scatter(df,
                            x='Fixation X',
                            y='Fixation Y',
                            title='Fixation X and Y')

    fig_fixationstartend = px.scatter(df,
                            x='Fixation Start',
                            y='Fixation End',
                            title='Fixation Start and End')

    fig_velacc = px.scatter(df,
                            x='Saccade Peak Velocity',
                            y='Saccade Peak Acceleration',
                            title='Peak Velocity & Peak Acceleration')

    fig_accdel = px.scatter(df,
                            x='Saccade Peak Deceleration',
                            y='Saccade Peak Acceleration',
                            title='Peak Deceleration & Peak Acceleration')

    fig_durdir = px.scatter(df,
                            x='Saccade Direction',
                            y='Saccade Duration',
                            title='Duration & Direction')
                    
    fig_ampvel = px.scatter(df,
                            x='Saccade Amplitude',
                            y='Saccade Peak Velocity',
                            title='Amplitude & Peak Velocity')

    fig_blink = px.histogram(df,
                        x='Blink detected (binary)',
                        title='Detected blinks',
                        nbins=2)


    # the layout
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
                                dcc.Graph(figure=fig_3dgaze)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_pupilscat)
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
                                dcc.Graph(figure=fig_2dgazeinter)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_gazevelacc)
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
                                dcc.Graph(figure=fig_fixationxy)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_fixationstartend)
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
                html.H4('Saccade'),
                html.P(f"""- Duration (hoe lang duurt de beweging van het oog tussen de fixation points)
                    - Amplitude (hoekafstand die de ogen van het beginpunt naar het eindpunt hebben afgelegd)
                    - Peak velocity (de maximale snelheid van de ogen tijdens deze saccade)
                    - Peak acceleration (de maximale snelheidstoename van de ogen tijdens deze saccade)
                    - Peak deceleration (maximale afname van de snelheid van de ogen tijdens deze saccade)
                    - Direction (richting van de saccade van het beginpunt naar het eindpunt, aangegeven als hoeken tegen de klok in: 0 graden betekent een horizontale saccade van links naar rechts, 90 graden een verticale saccade van onder naar boven)
                """),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_velacc)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_accdel)
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
                                dcc.Graph(figure=fig_durdir)
                            ]
                        ),
                        dbc.Col(
                            width=6,
                            children=
                            [
                                dcc.Graph(figure=fig_ampvel)
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

    fig_xbar = px.bar(df,
                x='ET_GazeDirectionLeftX',
                y='ET_GazeDirectionRightX')

    fig_xcolumn = px.line(df,
                x='ET_GazeDirectionLeftX',
                y='ET_GazeDirectionRightX')

    fig_xline = px.line(df,
                x='ET_GazeDirectionLeftX',
                y='ET_GazeDirectionRightX')

    fig_ybar = px.bar(df,
                x='ET_GazeDirectionLeftY',
                y='ET_GazeDirectionRightY')

    fig_ycolumn = px.line(df,
                x='ET_GazeDirectionLeftY',
                y='ET_GazeDirectionRightY')

    fig_yline = px.line(df,
                x='ET_GazeDirectionLeftY',
                y='ET_GazeDirectionRightY')

    fig_zbar = px.bar(df,
                x='ET_GazeDirectionLeftZ',
                y='ET_GazeDirectionRightZ')

    fig_zcolumn = px.line(df,
                x='ET_GazeDirectionLeftZ',
                y='ET_GazeDirectionRightZ')

    fig_zline = px.line(df,
                x='ET_GazeDirectionLeftZ',
                y='ET_GazeDirectionRightZ')

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
        ),
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('Direction'),
                html.P(f'Information'),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_xbar)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_xcolumn)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_xline)
                            ]
                        ),

                    ]
                ),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_ybar)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_ycolumn)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_yline)
                            ]
                        ),

                    ]
                ),
                dbc.Row(
                    children=
                    [
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_zbar)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_zcolumn)
                            ]
                        ),
                        dbc.Col(
                            width=4,
                            children=
                            [
                                dcc.Graph(figure=fig_zline)
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
    return tab_layout