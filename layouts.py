import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from styles import *
from graphs import *


def main_page(app, visible):
    main_page = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(
                    html.Img(src=app.get_asset_url("banner.webp"), style={
                             "max-width": "100%", "height": "auto", "width": "55%"}),
                style={"display": "flex", "justify-content": "center"})
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
                    dbc.CardBody([
                        html.H3("KPI"),
                        html.P(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam."),
                        dbc.Button("Go there", color="dark", id="button-kpi")
                    ])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H3("Cluster"),
                        html.P(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam."),
                        dbc.Button("Go there", color="dark",
                                   id="button-cluster")
                    ]),
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H3("Resultado"),
                        html.P(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam."),
                        dbc.Button("Go there", color="dark",
                                   id="button-result")
                    ])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H3("XXI"),
                        html.P(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam."),
                        dbc.Button("Go there", color="dark", id="button-xxi")
                    ])
                ], color="warning", outline=True)
            ),
        ], className="m-4")
    ], style={"display": "block" if visible else "none", "background-color": "#efe8df"})

    return main_page


def sidebar(visible):
    SIDEBAR_STYLE["display"] = "block" if visible else "none"
    sidebar = html.Nav(
        [
            html.H4("Menú", className="lead navbar-brand"),  # display-4
            html.Hr(),  # Esto es una línea horizontal que separa lo de arriba
            html.Div(
                [
                    dbc.Button("Main", id="link-hoja-main", className="btn btn-warning m-1"),
                    dbc.Button("KPI's", id="link-hoja-1", className="btn btn-warning m-1"),
                    dbc.Button("Clustering: definición", id="link-hoja-2", className="btn btn-warning m-1"),
                    dbc.Button("Clustering: resultados", id="link-hoja-3", className="btn btn-warning m-1"),
                ],
            ),
        ], style=SIDEBAR_STYLE, className="navbar navbar-dark bg-dark"
    )
    return sidebar

graphs = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graf6", figure=graf6)
        ]),
        dbc.Col([
            tabla1
        ]),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                placeholder="Options",
                id="date_dropdown",
                value="year_factura",
                className="dropdow  n",
                options=[
                    {"label": "Year", "value": "year"},
                    {"label": "Trim Año", "value": "trim_año"},
                    {"label": "Year Factura", "value": "year_factura"},
                ])
        ),
        dbc.Col([
            dbc.RadioItems(
                id="radio_items",
                value="vlr_neto",
                options=[
                    {"label": "vlr_neto", "value": "vlr_neto"},
                    {"label": "qt_facturas", "value": "qt_facturas"}
                ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graf1", figure=graf1)
        ]),

        dbc.Col([
            dcc.Graph(id="graf3", figure=graf3,
                      style={"margin-left": "10rem"}),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graf0", figure=graf0)
        ]),
        dbc.Col([
            dcc.Graph(id="graf5", figure=graf5)
        ]),
    ])
])