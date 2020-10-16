import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from styles import *


def main_page(app):
    main_page = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(
                    html.Img(src=app.get_asset_url("banner.webp")),
                    style={
                        "position": "absolute",
                        "background-color": "#0F0",
                        "display": "inline-block"
                    })
            ])
        ]),
    ])
    return main_page


def sidebar():
    sidebar = html.Div(
        [
            html.H4("Menú", className="lead"),  # display-4
            html.Hr(),  # Esto es una línea horizontal que separa lo de arriba
            html.P(
                "Navegar al elemento deseado", className="lead"  # Esto es un elemento de párrafo
            ),
            dbc.Nav(
                [
                    dbc.NavLink(
                        "Main", href="http://127.0.0.1:8050/main", id="link_main"),
                    dbc.NavLink(
                        "KPI's", href="http://127.0.0.1:8050/hoja-1", id="link_hoja_1"),
                    dbc.NavLink("Clustering: definición",
                                href="http://127.0.0.1:8050/hoja-2", id="link_hoja_2"),
                    dbc.NavLink("Clustering: resultados",
                                href="/hoja-3", id="link_hoja_3"),
                ],
                vertical=True,  # Esto para qué?
                pills=True,  # Esto para qué?
            ),
        ], style=SIDEBAR_STYLE,
    )
    return sidebar
