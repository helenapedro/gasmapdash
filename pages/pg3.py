import pandas as pd
import requests
import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px

dash.register_page(__name__,
                   path='/mapdata',
                   name='Map Data',
                   title='Map',
                   image='pg3.png',
                   description='Learn all about the heatmap.'
)

def fetch_data():
    url = "https://gaspump-18b4eae89030.herokuapp.com/api/stations"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df


# Layout of the Dash app
layout = html.Div([
    html.H1("Gas Station Data (Map)"),
    dcc.Graph(id='gas-stations-map'),  # Add a Graph component for the map
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
])

@callback(
    Output('gas-stations-map', 'figure'),  # Update the figure of the map
    [Input('interval-component', 'n_intervals')]
)
def update_map(n_intervals):
    df = fetch_data()
    
    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                            hover_name='Municipality',
                            hover_data=['Station', 'Address'],
                            zoom=5, height=600)
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig