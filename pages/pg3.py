import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import requests
import pandas as pd

dash.register_page(__name__,
                   path='/mapdata',
                   name='Map',
                   title='MapData'
)

def fetch_data():
    url = "https://gaspump-18b4eae89030.herokuapp.com/api/stations"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

layout = html.Div([
    dcc.Dropdown(
        id='address-dropdown',
        options=[{'label': address, 'value': address} for address in fetch_data()['Address']],
        placeholder="Select an Address"
    ),
    dcc.Graph(id='gas-stations-map'),  # Add a Graph component for the map
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
])

@callback(
    Output('gas-stations-map', 'figure'),  # Update the figure of the map
    [Input('interval-component', 'n_intervals'),
     Input('address-dropdown', 'value')]
)
def update_map(n_intervals, selected_address):
    df = fetch_data()
    if selected_address:
        selected_row = df[df['Address'] == selected_address]
        
        # Extract latitude and longitude of selected address
        selected_lat = selected_row['Latitude'].iloc[0]
        selected_lon = selected_row['Longitude'].iloc[0]
        
        # Update map to center on the selected address
        fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                                hover_name='Municipality',
                                hover_data=['Station', 'Address'],
                                zoom=8, height=600)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(mapbox_center={"lat": selected_lat, "lon": selected_lon})
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig
    else:
        fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                                hover_name='Municipality',
                                hover_data=['Station', 'Address'],
                                zoom=5, height=600)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig

