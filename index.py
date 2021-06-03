"""
For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import pandas as pd
from logging import disable
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from layouts.layout_global import header, sidebar
from callbacks import toggle_filter_collapse

# Load in the data
print('loading df...')
df = pd.read_csv('./data/Data_all_respondents.csv', low_memory=False, index_col='Unnamed: 0')
print(df)


# Content section (plots go here)
content = html.Section(id='page-content')

# Main (header + content wrapper)
main = html.Main(
    [
        header,
        content,
    ],
    id='main'
)

# Full layout (all html elements combined)
app.layout = html.Div(
    [
        # head
        dcc.Location(id="url"), 
        dcc.Store(id='data-storage', storage_type='session'),     # data/filters stored in Store

        # body
        sidebar, 
        main
    ]
)

# Callbacks ----------------------------------------------------------------------------------------------------------------------
# Page content based on sidebar nav & Store (filter) 
@app.callback([Output('page-content', 'children'),
               Output('page-title', 'children'),
               Output('nav-dropdown', 'className')], 
               [Input("url", "pathname"),
                Input('data-storage', 'data')])        # Store (contains filters)
def render_page_content(pathname, data):
    # Applying the respondent filters to the df
    print('copying df:...')
    dff = df.copy()
    print('showing filtered df:...')
    print(dff[dff['Resp gender'].isin(data['gender'])].head())

    # Page: Home
    if pathname == "/":
        return html.Div(
            [
                html.P("This is the content of the home page!"),
                html.P(data['gender'])
            ]
        ), 'Home', ''
    
    # Page: Data full route
    elif pathname == "/full-route":
        return html.P("This is the data of the full route. Yay!"), 'Data full route', ''
    
    # Page: Data per viewpoint
    elif pathname in ["/per-viewpoint-1", "/per-viewpoint-2"]:
        return html.P("This is the data per viewpoint."), 'Data per viewpoint', 'show'

    # Page: 404
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ], 'Error 404', ''
    )

if __name__ == "__main__":
    app.run_server(debug=True)