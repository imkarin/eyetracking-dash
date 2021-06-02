"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
mand
"""
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
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
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
                dbc.Col(html.H2("Home"),
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
@app.callback(Output("page-content", "children"), 
            [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(        
            [
                html.P("This is the content of the home page!"),
            ]
        )
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

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