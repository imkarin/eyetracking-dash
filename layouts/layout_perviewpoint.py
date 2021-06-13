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
                            )\
                            .update_traces(marker={'color':'yellow', 'size': 10})

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
                        # Add fixation plots...
                    ]
                ),
            ]
        ),
    ]
    return tab_layout

# Tab 2: GSR
def tab_gsr(df):
    # reltime = pd.Series()

    # for resp in df['Resp name'].unique():
    #     # vp1 = df[df['Resp name'] == resp][df['Viewpoint_1 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'] - df[df['Resp name'] == resp][df['Viewpoint_1 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'].iloc[0]
    #     # vp2 = df[df['Resp name'] == resp][df['Viewpoint_2 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'] - df[df['Resp name'] == resp][df['Viewpoint_2 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'].iloc[0]
    #     vp3 = df[df['Resp name'] == resp][df['Viewpoint_3 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'] - df[df['Resp name'] == resp][df['Viewpoint_3 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'].iloc[0]
    #     vp4 = df[df['Resp name'] == resp][df['Viewpoint_4 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'] - df[df['Resp name'] == resp][df['Viewpoint_4 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'].iloc[0]
    #     # vp5 = df[df['Resp name'] == resp][df['Viewpoint_5 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'] - df[df['Resp name'] == resp][df['Viewpoint_5 active on Tobii Glasses 2 Scene'] == 1]['Timestamp'].iloc[0]
    # reltime = pd.concat([reltime, vp1, vp2, vp3, vp4])
    
    # df['Relative timestamp'] = reltime


    # GSR Raw
    fig_gsrraw = px.line(df.sort_values('Timestamp'),
                         y='GSR Raw (microSiemens)',
                         x='Relative timestamp',
                         color='Resp name',
                         title='GSR over time'
                         )

    # Tonic signal
    fig_tonic = px.line(df.sort_values('Timestamp'),
                         y='Tonic signal (microSiemens)',
                         x='Timestamp',
                         color='Resp name',
                         title='Tonic signal over time'
                         )
    # Phasic signal
    fig_phasic = px.line(df.sort_values('Timestamp'),
                         y='Phasic signal (microSiemens)',
                         x='Timestamp',
                         color='Resp name',
                         title='Phasic signal over time'
                         )
    
    # Peaks
    fig_peaks_detect = px.line(df.sort_values('Timestamp'),
                        y='Peak detected (binary)',
                        x='Timestamp',
                        color='Resp name',
                        title='Peaks detected over time'
                        )

    fig_peaks_amp = px.line(df.sort_values('Timestamp'),
                        y='Peak amplitude (microSiemens)',
                        x='Timestamp',
                        color='Resp name',
                        title='Peaks detected over time'
                        )

    tab_layout = [
        html.Section(
            className='mt-5',
            children=
            [
                html.H4('GSR Raw'),
                html.P(f'Information'),
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
                )
            ]
        ),

        html.Section(
            children=
            [
                html.H4('GSR Peaks'),
                html.P(f'Information'),
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
                x='Timestamp',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)

    fig_gyry = px.scatter(df,
                y='ET_GyroY',
                x='Timestamp',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)
                

    fig_gyrz = px.scatter(df,
                y='ET_GyroZ',
                x='Timestamp',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)


    fig_accx = px.scatter(df,
                y='ET_AccX',
                x='Timestamp',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)


    fig_accy = px.scatter(df,
                y='ET_AccY',
                x='Timestamp',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)


    fig_accz = px.scatter(df,
                y='ET_AccZ',
                x='Timestamp',
                color='Resp name',
                opacity=0.3).update_traces(marker_size=2)




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
    fig_int = px.scatter(df,
                        y='ET_DistanceLeft',
                        x='Timestamp',
                        opacity=0.3,
                        color='Resp name',
                        title='Distance')

    fig_pupilscat = px.scatter(df,
                                x='Timestamp',
                                y='ET_PupilLeft',
                                title='Pupil size',
                                color='Resp name',
                                opacity=0.3,
                                # labels={
                                #     "ET_PupilLeft": "Pupil left (mm)",
                                #     "ET_PupilRight": "Pupil right (mm)"}
                                )

    fig_val = px.scatter(df,
                        x='Timestamp',
                        y='ET_ValidityLeftEye',
                        color='Resp name',
                        opacity=0.3,
                        title='Eye Validity (left)')

    # fig_eye3d = px.scatter_3d(df,
    #             x='ET_DistanceLeft',
    #             y='ET_DistanceRight',
    #             z='ET_Distance3D')

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
                            width=12,
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