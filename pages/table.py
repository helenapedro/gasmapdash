import dash
from dash import html, dcc, dash_table, callback, State, Output, Input
import pandas as pd
import requests

dash.register_page(__name__,
                   path='/tabledata',  # represents the URL text
                   name='Table Data',  # name of the page, commonly used as the name of the link
                   title='Table'  # represents the title of the browser's tab
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
    dash_table.DataTable(
        id='table',
        columns=[
            {"name": "Operator", "id": "Operator", "deletable": True},
            {"name": "Station", "id": "Station", "deletable": True},
            {"name": "Address", "id": "Address", "deletable": True},
            {"name": "Municipality", "id": "Municipality", "deletable": True},
            {"name": "Latitude", "id": "Latitude", "deletable": True},
            {"name": "Longitude", "id": "Longitude", "deletable": True},
            {"name": "Province", "id": "Province", "deletable": True},
            {"name": "Country", "id": "Country", "deletable": True},
        ],
        style_table={'height': '500px', 'overflowY': 'auto'},
        style_cell={'padding': '10px', 'textAlign': 'center'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
        row_selectable='multi',  # Allow multiple row selection
        selected_rows=[],  # Initially no rows are selected
        page_action='native',  # Enable pagination
        page_size=25,  # Show 10 rows per page
        export_format="csv",  # Allow CSV export
    ),
])

# Callback to update the data in the table based on selected municipality
@callback(
    Output('table', 'data'),
    Input('municipality-dropdown', 'value')
)
def update_table(selected_municipality):
    df = fetch_data()
    if selected_municipality:
        df = df[df['Municipality'] == selected_municipality]
    return df.to_dict('records')

# Callback to trigger CSV export
@callback(
    Output("table", "exportDataAsCsv"),
    Input("csv-button", "n_clicks"),
)
def export_data_as_csv(n_clicks):
    if n_clicks:
        return True
    return False

# Callback to handle row selection
@callback(
    Output("clipboard", "content"),
    Input("table", "selected_rows"),
    State("table", "data")
)
def copy_selected_rows(selected_rows, data):
    if not selected_rows:
        return "No selections"
    
    # Get the selected rows from the data
    selected_data = [data[i] for i in selected_rows]
    df_selected = pd.DataFrame(selected_data)
    return df_selected.to_string()

