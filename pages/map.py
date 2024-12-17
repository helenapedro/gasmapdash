import dash
from dash import dcc, html, callback, Input, Output
import plotly.express as px
import requests
import pandas as pd

dash.register_page(__name__,
                   path='/',
                   name='Map',
                   title='Home'
)

# Function to fetch data
def fetch_data():
    url = "https://gaspump-18b4eae89030.herokuapp.com/api/stations"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

# Layout
layout = html.Div([
    # Notification Banner
    html.Div(
        "Note: This map does not yet include the complete list of gas stations.",
        style={
            'backgroundColor': '#ffcccb',
            'color': '#800000',
            'padding': '10px',
            'marginBottom': '10px',
            'borderRadius': '5px',
            'fontWeight': 'bold',
            'textAlign': 'center'
        }
    ),
    # Dropdown for selecting address
    dcc.Dropdown(
        id='address-dropdown',
        options=[{
            'label': address, 
            'value': address} for address in fetch_data()['Address']
        ],
        placeholder="Select an Address",
        style={'marginBottom': '15px'}
    ),
    # Map Display
    dcc.Graph(id='gas-stations-map'), 
    # Auto-refresh Interval
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update map
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
        
        # Highlight selected gas station
        fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                                hover_name='Municipality',
                                hover_data=['Station', 'Address'],
                                zoom=12, height=600)
        fig.add_scattermapbox(
            lat=[selected_lat],
            lon=[selected_lon],
            mode='markers',
            marker=dict(size=14, color='red', symbol='circle'),
            name='Selected Station'
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(mapbox_center={"lat": selected_lat, "lon": selected_lon})
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig
    else:
        # Default map view
        fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude',
                                hover_name='Municipality',
                                hover_data=['Station', 'Address'],
                                zoom=5, height=600)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        return fig
