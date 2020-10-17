import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from styles import *


def main_page(app):
    main_page = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(
                    html.Img(src=app.get_asset_url("banner.webp"), style={
                             "max-width": "100%", "height": "auto"}),
                )
            ])
        ]),
        dbc.Row(
            dbc.Col(
                html.P("Lorem ipsum dolor sit amet, \
                    consectetur adipiscing elit. Sed ac fringilla tortor. \
                    Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; \
                    Duis lorem est, commodo quis molestie sed, \
                    cursus vel purus. Nunc eu urna eget neque sollicitudin ultrices. Ut libero tortor, \
                    pretium at tristique vitae, pretium vitae neque. Ut vestibulum mi sit amet odio vestibulum tristique. \
                    Maecenas accumsan aliquet lacus, ut dignissim mi gravida in. In at libero volutpat, iaculis tortor sed, \
                    dignissim felis. Pellentesque dictum molestie euismod. Mauris a efficitur justo. \
                    Vestibulum posuere fringilla sem sed gravida. ")
            ), className="m-3"
        ),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([html.H3("KPI"), html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam.")])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([html.H3("Cluster"), html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam.")])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([html.H3("Resultado"), html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam.")])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([html.H3("XXI"), html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam.")])
                ], color="warning", outline=True)
            ),
        ], className="m-4")
    ])

    @app.callback()
    def click_kpi():
        pass


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
