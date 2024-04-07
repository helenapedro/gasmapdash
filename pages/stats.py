import dash
from dash import html, dcc, callback, Output, Input
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
import requests

dash.register_page(__name__,
                   path='/stats',
                   name='Statistics',
                   title='Stats'
)

# Function to fetch data from the API with error handling
def fetch_data():
    try:
        url = "https://gaspump-18b4eae89030.herokuapp.com/api/stations"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad response status
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Function to get unique municipalities from the data
def get_unique_municipalities():
    df = fetch_data()
    return df['Municipality'].unique() if not df.empty else []

# Layout of the Dash app
layout = html.Div([
    # Total Gas Stations
    html.Div(id='total-gas-stations'),
    
    # Operator Distribution
    html.Div([
        dcc.Graph(id='operator-distribution')
    ]),
    
    # Municipality Distribution
    html.Div([
        dcc.Graph(id='municipality-distribution')
    ])

])

# Callbacks for interactive elements
@callback(
    Output('total-gas-stations', 'children'),
    Output('operator-distribution', 'figure'),
    Output('municipality-distribution', 'figure'),
    Input('operator-distribution', 'value'),
    Input('municipality-distribution', 'value')
)
def update_graph(operator, municipality):
    df = fetch_data()  # Fetch data within the callback to get the latest data
    if df.empty:
        return "Error fetching data", {}, {}

    # Calculate total gas stations dynamically
    total_gas_stations = len(df)
    
    # Generate Operator Distribution Plot
    operator_counts = df['Operator'].value_counts()
    operator_fig = px.bar(operator_counts, x=operator_counts.index, y=operator_counts.values, 
                          labels={'x': 'Operator', 'y': 'Count'}, 
                          title='Operator Distribution')
    
    # Generate Municipality Distribution Plot
    municipality_counts = df['Municipality'].value_counts()
    municipality_fig = px.bar(municipality_counts, x=municipality_counts.index, y=municipality_counts.values, 
                              labels={'x': 'Municipality', 'y': 'Count'}, 
                              title='Municipality Distribution')
    
    return f"Total Gas Stations: {total_gas_stations}", operator_fig, municipality_fig