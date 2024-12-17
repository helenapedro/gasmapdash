import dash
from dash import html, dcc, callback, Output, Input
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

# Layout of the Dash app
layout = html.Div([
    # Main Container with Padding and Centering
    html.Div([
        # Total Gas Stations
        html.Div(id='total-gas-stations', style={'fontSize': '24px', 'fontWeight': 'bold', 'marginBottom': '20px'}),

        # Additional Statistics
        html.Div(id='additional-statistics', style={'fontSize': '18px', 'marginBottom': '20px'}),

        # Section with Dropdowns in a Row
        html.Div([
            html.Div([
                html.Label("Select Province:"),
                dcc.Dropdown(id='province-dropdown', style={'width': '100%'}),
            ], style={'flex': '1', 'paddingRight': '10px'}),

            html.Div([
                html.Label("Select Municipality:"),
                dcc.Dropdown(id='municipality-dropdown', style={'width': '100%'}),
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),

        # Graphs Section with Proper Spacing
        html.Div([
            # Municipality Distribution Graph
            html.Div([
                dcc.Graph(id='municipality-distribution'),
            ], style={'marginBottom': '20px'}),

             # Operator Distribution Graph
            html.Div([
                dcc.Graph(id='operator-distribution'),
            ], style={'marginBottom': '20px'}),

        ]),

    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'}),
])


# Callback to populate province dropdown
@callback(
    Output('province-dropdown', 'options'),
    Input('province-dropdown', 'value')
)
def update_province_dropdown(selected_province):
    df = fetch_data()
    if not df.empty:
        return [{'label': province, 'value': province} for province in df['Province'].unique()]
    else:
        return []

# Callback to populate municipality dropdown based on selected province
@callback(
    Output('municipality-dropdown', 'options'),
    Input('province-dropdown', 'value')
)
def update_municipality_dropdown(selected_province):
    if selected_province:
        df = fetch_data()[fetch_data()['Province'] == selected_province]
        return [{'label': municipality, 'value': municipality} for municipality in df['Municipality'].unique()]
    else:
        return []

# Callback to update graphs based on selected province and municipality
@callback(
    Output('total-gas-stations', 'children'),
    Output('additional-statistics', 'children'),
    Output('operator-distribution', 'figure'),
    Output('municipality-distribution', 'figure'),
    Input('province-dropdown', 'value'),
    Input('municipality-dropdown', 'value')
)
def update_graph(selected_province, selected_municipality):
    df = fetch_data()  # Fetch data within the callback to get the latest data
    if df.empty:
        return "Error fetching data", "", {}, {}

    filtered_df = df
    if selected_province:
        filtered_df = filtered_df[filtered_df['Province'] == selected_province]
    if selected_municipality:
        filtered_df = filtered_df[filtered_df['Municipality'] == selected_municipality]

    total_gas_stations = len(filtered_df)

    # Additional Statistics
    num_operators = filtered_df['Operator'].nunique()
    num_municipalities = filtered_df['Municipality'].nunique()
    additional_stats = f"Unique Operators: {num_operators} | Unique Municipalities: {num_municipalities}"

    # Operator Distribution
    operator_counts = filtered_df['Operator'].value_counts()
    operator_fig = px.bar(operator_counts, x=operator_counts.index, y=operator_counts.values,
                          labels={'x': 'Operator', 'y': 'Count'},
                          title='Operator Distribution')

    # Municipality Distribution
    municipality_counts = filtered_df['Municipality'].value_counts()
    municipality_fig = px.bar(municipality_counts, x=municipality_counts.index, y=municipality_counts.values,
                              labels={'x': 'Municipality', 'y': 'Count'},
                              title='Municipality Distribution')

    return f"Total Gas Stations: {total_gas_stations}", additional_stats, operator_fig, municipality_fig
