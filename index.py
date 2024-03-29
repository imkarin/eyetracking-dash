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
from layouts.layout_global import layout_global
from layouts.layout_home import layout_home
from layouts.layout_fullroute import layout_fullroute
from layouts.layout_perviewpoint import layout_perviewpoint
from layouts.layout_sources import layout_sources

import base64

# Load in the data (smaller version for development)
print('Loading df...')
df = pd.read_csv('./data/Data_all_respondents.csv', low_memory=True, index_col='Unnamed: 0')
df = df.sort_values('Timestamp')

# Df preparation
df = df.reset_index(drop=True)
df['Resp rec datetime'] = pd.to_datetime(df['Resp rec datetime'])

# Content section (plots go here)
content = html.Section(id='page-content')

# Main (header + content wrapper)
main = html.Main(
    [
        layout_global(df)[1],  # <-- header
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
        layout_global(df)[0], # <-- sidebar 
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
    # dff = df.copy()

    # Respondent filters:
    gender_filter = (df['Resp gender'].isin(data['gender']))
    age_filter = (df['Resp age'].isin(data['age']))
    timebegin = pd.to_datetime(data['time'][0], errors='coerce')
    timeend = pd.to_datetime(data['time'][1], errors='coerce')
    
    if(type(timebegin) != pd.Timestamp or type(timeend) != pd.Timestamp):    # Check if begin/endtime is timestamp
        time_filter = True
    else:
        time_filter = ((df['Resp rec datetime'].dt.time >= timebegin.time()) 
                    & (df['Resp rec datetime'].dt.time <= timeend.time()))

    dff = df[gender_filter & age_filter & time_filter]

    # If respondent filters don't match anything, don't update
    if (len(dff) == 0):
        raise PreventUpdate

    # If 'data per viewpoint' is chosen, check which VP:
    if pathname == '/viewpoint-1':
        dff = dff[dff['Viewpoint_1 active on Tobii Glasses 2 Scene'] == 1]

        image_filename = 'assets/img/Viewport_Panorama-1.jpg'
        bgimg = base64.b64encode(open(image_filename, 'rb').read())
        width = 709 * 1.2
        height = 400 * 1.2
    elif pathname == '/viewpoint-2':
        dff = dff[dff['Viewpoint_2 active on Tobii Glasses 2 Scene'] == 1]

        image_filename = 'assets\img\Viewport_Panorama-2.jpg'
        bgimg = base64.b64encode(open(image_filename, 'rb').read())
        width = 513 * 1.2
        height = 394 * 1.2
    elif pathname == '/viewpoint-3':
        dff = dff[dff['Viewpoint_3 active on Tobii Glasses 2 Scene'] == 1]

        image_filename = 'assets\img\Viewport_Panorama-3.jpg'
        bgimg = base64.b64encode(open(image_filename, 'rb').read())
        width = 425 * 1.3
        height = 356 * 1.3
    elif pathname == '/viewpoint-4':
        dff = dff[dff['Viewpoint_4 active on Tobii Glasses 2 Scene'] == 1]

        image_filename = 'assets\img\Viewport_Panorama-4.jpg'
        bgimg = base64.b64encode(open(image_filename, 'rb').read())
        width = 456 * 1.4
        height = 314 * 1.4
    elif pathname == '/viewpoint-5':
        dff = dff[dff['Viewpoint_5 active on Tobii Glasses 2 Scene'] == 1]

        image_filename = 'assets\img\Viewport_Panorama-5.jpg'
        bgimg = base64.b64encode(open(image_filename, 'rb').read())
        width = 558 * 1.4
        height = 226 * 1.4

    print('Chosen respondents:')
    print(dff['Resp name'].unique())


    # If filters don't match anything, don't update
    if (len(dff) == 0):
        print("Didn't update plots, no data that matches the filters.")
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
        return layout_perviewpoint(dff, pathname, bgimg, width, height), 'Data per viewpoint', 'show'

    # Page: Sources
    elif pathname == "/sources":
        return layout_sources(), 'Sources', ''

    # Page: 404
    return [dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )], 'Not found', ''

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)