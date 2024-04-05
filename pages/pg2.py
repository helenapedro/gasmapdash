import dash
from dash import html, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import requests

dash.register_page(__name__,
                   path='/',  # represents the url text
                   name='Table',  # name of page, commonly used as name of link
                   title='Gas Stations Table'  # represents the title of browser's tab
)

# Function to fetch data from the API
def fetch_data():
    url = "https://gaspump-18b4eae89030.herokuapp.com/api/stations"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

categories = ['Station', 'Address', 'Municipality', 'Latitude', 'Longitude', 'Province', 'Country']
# Layout of the Dash app
layout = html.Div([
    dag.AgGrid(
        id='ag-grid',
        columnDefs=[
            {'field': 'Operator', 'filter': True},
            {'field': 'Station'},
            {'field': 'Address'},
            {'field': 'Municipality', 'filter': True},
            {'field': 'Province', 'filter': True},
            {'field': 'Country'},
            {
                'headerName': 'Municipality', 
                "cellClass": 'center-aligned-cell',
                'children': [
                                {'field': "Latitude"},
                                {'field': "Longitude"},
                            ]
            },
        ],
        defaultColDef = {"headerClass": 'center-aligned-header'},
        columnSize="sizeToFit",
    )
])

# Callback to update the data in the table
@callback(
    Output('ag-grid', 'rowData'),
    Input('ag-grid', 'page_size')
)
def update_table(page_size):
    df = fetch_data()
    return df.to_dict("records")
