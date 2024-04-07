import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

navbar = dbc.NavbarSimple(
    brand="GasPump Data Map",
    brand_href="/",
    color="#802917",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("Map", href="/")),
        dbc.NavItem(dbc.NavLink("Table", href="/tabledata")),
        dbc.NavItem(dbc.NavLink("Stats", href="/stats")),
    ],
)

app.layout = dbc.Container([
    navbar,

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    dash.page_container
                ], xs=12, sm=12, md=12, lg=12, xl=12, xxl=12)
        ]
    ),

    html.Hr(),

    # Footer
    html.Footer([
        html.Div(html.A("Helena Pedro", href="https://helenapedro.github.io/", target="_blank")),
        html.Div("© 2024")
    ])

], fluid=True)



if __name__ == "__main__":
    app.run(debug=False)
