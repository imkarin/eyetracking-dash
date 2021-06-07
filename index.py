"""
For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from callbacks import toggle_filter_collapse, update_filters
from layouts.layout_global import header, sidebar
from layouts.layout_home import layout_home
from layouts.layout_fullroute import layout_fullroute
from layouts.layout_perviewpoint import layout_perviewpoint
import layouts.layout_sources

# Load in the data (smaller version for development)
print('Loading df...')
df = pd.read_csv('./data/Data_all_respondents.csv', low_memory=False, index_col='Unnamed: 0')
# df = pd.read_csv('./data/Data_all_resp_SMALL.csv', low_memory=False, index_col='Unnamed: 0')

# Df preparation
df = df.reset_index(drop=True)
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
    # Apply the new filters (new DF)
    dff = df.copy()
    if pathname == '/viewpoint-1':
        dff = dff[dff['Viewpoint_1 active on Tobii Glasses 2 Scene'] == 'Viewpoint_1']
    elif pathname == '/viewpoint-2':
        dff = dff[dff['Viewpoint_2 active on Tobii Glasses 2 Scene'] == 'Viewpoint_2']
    elif pathname == '/viewpoint-3':
        dff = dff[dff['Viewpoint_3 active on Tobii Glasses 2 Scene'] == 'Viewpoint_3']
    elif pathname == '/viewpoint-4':
        dff = dff[dff['Viewpoint_4 active on Tobii Glasses 2 Scene'] == 'Viewpoint_4']
    elif pathname == '/viewpoint-5':
        dff = dff[dff['Viewpoint_5 active on Tobii Glasses 2 Scene'] == 'Viewpoint_5']

    gender_filter = (dff['Resp gender'].isin(data['gender']))
    age_filter = (dff['Resp age'].isin(data['age']))
    timebegin = pd.to_datetime(data['time'][0], errors='coerce')
    timeend = pd.to_datetime(data['time'][1], errors='coerce')
    
    if(type(timebegin) != pd.Timestamp or type(timeend) != pd.Timestamp):    # Check if begin/endtime is timestamp
        time_filter = True
    else:
        time_filter = ((dff['Resp rec datetime'].dt.time >= timebegin.time()) 
                    & (dff['Resp rec datetime'].dt.time <= timeend.time()))

    dff = dff[gender_filter & age_filter & time_filter]

    # If filters don't match anything, don't update
    if (len(dff) == 0):
        raise PreventUpdate


    # Return new page content, with plots based on new DF
    # Page: Home
    if pathname == "/":
        return layout_home(dff), 'Home', ''
    
    # Page: Data full route
    elif pathname == "/full-route":
        return layout_fullroute(dff), 'Data full route', ''
    
    # Page: Data per viewpoint
    elif pathname in ["/viewpoint-1", "/viewpoint-2", "/viewpoint-3", "/viewpoint-4", "/viewpoint-5"]:
        return layout_perviewpoint(dff, pathname), 'Data per viewpoint', 'show'

    # Page: Sources
    elif pathname == "/sources":
        return html.P("This is the sources page."), 'Sources', ''

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