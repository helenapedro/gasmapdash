import dash
from dash import html, dcc, callback, State, Output, Input
import dash_ag_grid as dag
import pandas as pd
import requests

dash.register_page(__name__,
                   path='/tabledata',  # represents the url text
                   name='Table Data',  # name of page, commonly used as name of link
                   title='Table'  # represents the title of browser's tab
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
        return pd.DataFrame()

# Function to get unique municipalities from the data
def get_unique_municipalities():
    df = fetch_data()
    return df['Municipality'].unique()

# Layout of the Dash app
layout = html.Div([
    dcc.Dropdown(
        id='municipality-dropdown',
        options=[{'label': municipality, 'value': municipality} for municipality in get_unique_municipalities()],
        placeholder="Select a Municipality"
    ),
    html.Span("Copy selected "),
    dcc.Clipboard(id="clipboard", style={"display": "inline-block"}),
    dag.AgGrid(
        id='ag-grid',
        columnDefs=[
            {
                'field': 'Operator', 
                "checkboxSelection": True, 
                "headerCheckboxSelection": True
            },
            {'field': 'Station'},
            {'field': 'Address'},
            {"field": "Municipality"},
            {'field': "Latitude"},
            {'field': "Longitude"},
            {'field': "Province"},
            {'field': "Country"},
        ],
        defaultColDef = {"filter": True, "resizable": True, "suppressMovable": True},
        columnSize="sizeToFit",
        dashGridOptions={"pagination": True, "rowSelection": "multiple", "animateRows": False},
        csvExportParams={
            "fileName": "gaspump_data.csv",
        },
    ),
    html.Button("Download CSV", id="csv-button", n_clicks=0),
])

# Callback to update the data in the table based on selected municipality
@callback(
    Output('ag-grid', 'rowData'),
    Input('municipality-dropdown', 'value')
)
def update_table(selected_municipality):
    df = fetch_data()
    if selected_municipality:
        df = df[df['Municipality'] == selected_municipality]
    return df.to_dict("records")

# Callback to trigger CSV export
@callback(
    Output("ag-grid", "exportDataAsCsv"),
    Input("csv-button", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False

# Callback to copy selected rows to clipboard
@callback(
    Output("clipboard", "content"),
    Input("clipboard", "n_clicks"),
    State("ag-grid", "selectedRows"),
)
def selected(n, selected):
    if selected is None:
        return "No selections"
    df = fetch_data()
    df = df[["Station", "Address", "Latitude", "Longitude", "Municipality", "Province", "Country", "Operator"]]
    return df.to_string()