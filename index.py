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
import plotly.express as px

from app import app
from callbacks import toggle_filter_collapse, update_filters
from layouts.layout_global import header, sidebar
from layouts.layout_home import layout_home
from layouts.layout_fullroute import layout_fullroute
from layouts.layout_perviewpoint import layout_perviewpoint
import layouts.layout_sources

# Load in the data (smaller version for development)
print('Loading df...')
df = pd.read_csv('./data/Data_all_resp_SMALL.csv', low_memory=False, index_col='Unnamed: 0')
print(df)
df['Resp rec datetime'] = pd.to_datetime(df['Resp rec datetime'])


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
# PAGE 'ROUTING' / REFRESHING ON FILTER CHANGE
@app.callback([Output('page-content', 'children'),
               Output('page-title', 'children'),
               Output('nav-dropdown', 'className')], 
               [Input("url", "pathname"),
                Input('data-storage', 'data')])        # Store (contains filters)
def render_page_content(pathname, data):
    # Set the new DF: apply the new filters
    print('Showing filtered df...')
    dff = df.copy()

    gender_filter = (dff['Resp gender'].isin(data['gender']))
    age_filter = (dff['Resp age'].isin(data['age']))
    dff = dff[gender_filter & age_filter]


    # Return new page content, with plots based on new DF
    # Page: Home
    if pathname == "/":
        return layout_home(dff), 'Home', ''
    
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

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)