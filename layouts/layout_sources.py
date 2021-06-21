import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# HTML elements in the page-content section of the page: Sources
# This page has no tabs.
# This page might have no plots, so might not need a function but just an array of HTML elements.

def layout_sources():
    return html.Article([
        html.P("This dashboard was developed as a project for the Minor Data Science at the Amsterdam University of Applied Sciences. Its purpose is to support architects in their research on the influences of high-rise buildings on the residents' experiences and wellbeing."),
        html.P("The data used for this dashboard originates from Sensing Streetscapes and was gathered with the Tobii 2 Glasses Eyetracker and a GSR measurement system at the Zuidas in Amsterdam."),
        html.P("The data displayed on the dashboard is the raw data gathered from these eyetracking sessions. In the tabs 'Data quality', we show the validity of the data based on several indicators. Furthermore, the data visualizations are highly interactive, allowing the user to select only the data that they consider useful. We have chosen this approach so that the user has complete control over the data they wish to view, in order to be able to draw interesting and renewing conclusions for their research.")
    ])