import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from datetime import date

# HTML elements that occur in all pages (sidebar, header)
sidebar = html.Aside(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Data full route", href="/full-route", active="exact"),
                dbc.DropdownMenu(
                    id='nav-dropdown',
                    label="Data per viewpoint ",
                    in_navbar=True,
                    nav=True,
                    direction='right',
                    children=[
                        dbc.DropdownMenuItem(
                            dbc.NavLink("Viewpoint 1", href="per-viewpoint-1", active="exact")), 
                        dbc.DropdownMenuItem(
                            dbc.NavLink("Viewpoint 2", href="per-viewpoint-2", active="exact")
                        )],
                    ),
                dbc.NavLink("Sources", href="/sources", active="exact", disabled=True)
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className='sidebar',
)

header = html.Div(
    [
        dbc.Row(
            [   # Paginatitel
                dbc.Col(
                    width=4,
                    children=
                    [
                        html.H2(
                            "Home",
                            id="page-title"
                        ),
                    ]
                ),
                
                # Filter respondents (collapse)
                dbc.Col(
                    html.Div(
                        className='mb-4 d-flex flex-column align-items-end',
                        children=
                        [
                            dbc.Button(
                                "Filter respondents",
                                id="collapse-button",
                                className="mb-3",
                                color="primary",
                            ),
                            dbc.Collapse(
                                id="filter-collapse",
                                children=
                                [
                                    dbc.Card(
                                        className='px-3 pt-3 pb-2',
                                        children=
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Label(
                                                            [
                                                                html.P("Gender"),
                                                                dcc.Checklist(
                                                                    id='filter-gender-checklist',
                                                                    value=['MALE', 'FEMALE'],
                                                                    className='m-2',
                                                                    options=[
                                                                        {'label': 'MALE', 'value': 'MALE'},
                                                                        {'label': 'FEMALE', 'value': 'FEMALE'}
                                                                    ]
                                                                )
                                                            ],
                                                            className='filter-checklist'
                                                        ),
                                                        width=2
                                                    ),
                                                    dbc.Col(
                                                        html.Label(
                                                            [
                                                                html.P("Age"),
                                                                dcc.RangeSlider(
                                                                    id='filter-age-slider',
                                                                    className='m-2',
                                                                    value=[16, 18],
                                                                    min=16,
                                                                    max=18,
                                                                    step=1,
                                                                    marks={
                                                                        16: '16',
                                                                        17: '17',
                                                                        18: '18'
                                                                    }
                                                                )
                                                            ]
                                                        ),
                                                        width = 5,
                                                    ),
                                                    dbc.Col(
                                                        # width = 5,
                                                        children=
                                                        html.Div(
                                                            [
                                                                html.P("Time of recording"),
                                                                html.Div(
                                                                    className='d-flex flex-wrap justify-content-between',
                                                                    children=
                                                                    [
                                                                        html.Label(
                                                                            [
                                                                                html.P('Begin'),
                                                                                dcc.Input(
                                                                                    id='filter-timebegin-input',
                                                                                    type='text',
                                                                                    maxLength=5,
                                                                                    value="00:00",
                                                                                    placeholder="00:00"
                                                                                )
                                                                            ],
                                                                            className='d-flex justify-content-between mb-0',
                                                                        ),
                                                                        html.Label(
                                                                            className='d-flex flex-wrap justify-content-between',
                                                                            children=
                                                                            [
                                                                                html.P('End'),
                                                                                dcc.Input(
                                                                                    id='filter-timeend-input',
                                                                                    type='text',
                                                                                    maxLength=5,
                                                                                    value='23:59',
                                                                                    placeholder='23:59'
                                                                                )
                                                                            ]
                                                                        )
                                                                    ],
                                                                )
                                                            ],
                                                            className='filter-time-rec'
                                                        )
                                                    )
                                                ]  # End Row (filter controls)
                                            )
                                        ]
                                    ),  # End Card
                                ]
                            ), # End Collapse
                        ],
                    ), # End Div
                ) # End Col
            ]
        ) # End Row
    ]
) # End Div (Header)