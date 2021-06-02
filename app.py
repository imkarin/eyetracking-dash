"""
For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
from logging import disable
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

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
                dbc.NavLink("Data full route", href="/complete-route", active="exact"),
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
    style=SIDEBAR_STYLE,
)

header = html.Div(
    [
        dbc.Row(
            [   # Paginatitel
                dbc.Col(
                    html.H2(
                        "Home",
                        id="page-title"
                    ),
                ),
                
                # Filter respondents (collapse)
                dbc.Col(
                    html.Div(
                        [
                            dbc.Button(
                                "Filter respondents",
                                id="collapse-button",
                                className="mb-3",
                                color="primary",
                            ),
                            dbc.Collapse(
                                dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                                id="collapse"
                            ),
                        ],
                        className='mb-4 d-flex flex-column align-items-end'
                    ),
                )
            ]
        )
    ]
)

content = html.Main(
    [
        header,
        html.Div(id="page-content")
    ], 
    style=CONTENT_STYLE
)

app.layout = html.Div(
    [
        # head
        dcc.Location(id="url"), 

        # body
        sidebar, 
        content
    ]
)

# Callbacks ----------------------------------------------------------------------------------------------------------------------
# Page content based on sidebar links (nav)
@app.callback([Output('page-content', 'children'),
               Output('page-title', 'children'),
               Output('nav-dropdown', 'className')], 
               [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(        
            [
                html.P("This is the content of the home page!"),
            ]
        ), 'Home', ''
    elif pathname == "/complete-route":
        return html.P("This is the data of the full route. Yay!"), 'Data full route', ''
    elif pathname in ["/per-viewpoint-1", "/per-viewpoint-2"]:
        return html.P("This is the data per viewpoint."), 'Data per viewpoint', 'show'
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ], 'Error 404', ''
    )

# Filter collapse callback
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)