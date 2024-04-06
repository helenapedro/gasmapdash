import dash
from dash import html, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import requests

dash.register_page(__name__,
                   path='/',  # represents the url text
                   name='Table',  # name of page, commonly used as name of link
                   title='Home'  # represents the title of browser's tab
)

# Function to fetch data from the API
def fetch_data():
    url = "https://gaspump-18b4eae89030.herokuapp.com/api/stations"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

# Function to get unique municipalities from the data
def get_unique_municipalities():
    df = fetch_data()
    return df['Municipality'].unique()

categories = ['Station', 'Address', 'Municipality', 'Latitude', 'Longitude', 'Province']
# Layout of the Dash app
layout = html.Div([
    dcc.Dropdown(
        id='municipality-dropdown',
        options=[{'label': municipality, 'value': municipality} for municipality in get_unique_municipalities()],
        placeholder="Select a Municipality"
    ),
    dag.AgGrid(
        id='ag-grid',
        columnDefs=[
            {'field': 'Operator', 'filter': True, "pinned": True, "resizable": False},
            {
                'headerName': 'Operator Details',
                'children': [
                    {'field': 'Station'},
                    {'field': 'Address'},
                ]
            },
            {
                'headerName': 'Municipality Details',
                'children': [
                                {"field": "Municipality", 'filter': True},
                                {'field': "Latitude"},
                                {'field': "Longitude"},
                                {'field': "Province", 'filter': True},
                                {'field': "Country"},
                            ],
                'headerClass': 'center-aligned-header'
            },
        ],
        defaultColDef = {"headerClass": 'center-aligned-header'},
        columnSize="autoSize",
        dashGridOptions={"pagination": True, "animateRows": False},
    )
])

# Callback to update the data in the table based on selected municipality
@callback(
    Output('ag-grid', 'rowData'),
    Input('municipality-dropdown', 'value')
)
def update_table(selected_municipality):
    df = fetch_data()
    if selected_municipality is not None:
        df = df[df['Municipality'] == selected_municipality]
    return df.to_dict("records")
