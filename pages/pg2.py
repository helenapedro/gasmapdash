import pandas as pd
import dash
from dash import html, dash_table, callback, Output, Input
import requests

dash.register_page(__name__,
                   path='/table',  # represents the url text
                   name='Table',  # name of page, commonly used as name of link
                   title='Gas Stations Table'  # epresents the title of browser's tab
)

# Function to fetch data from the API
def fetch_data():
    url = "https://gaspump-18b4eae89030.herokuapp.com/api/stations"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

# Define column names for the DataTable
categories = ['Station', 'Address', 'Municipality', 'Province', 'Country']

# Layout of the Dash app
layout = html.Div([
    html.H1("Gas Station Data"),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container'),
    html.Div(id='choromap-container'),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[{"name": i, "id": i} for i in categories],
        filter_action="native",     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",     # allow users to select 'multi' or 'single' rows
        row_deletable=True,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=6,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'minWidth': 95, 'maxWidth': 95, 'width': 95
        },
        style_data={                # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto'
        }
    )
])

@callback(
    Output('datatable-interactivity', 'data'),
    [Input('datatable-interactivity', 'page_current'),
     Input('datatable-interactivity', 'page_size')]
)
def update_data(page_current, page_size):
    df = fetch_data()
    return df.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')

@callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]