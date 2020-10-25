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
        html.H3("Proyecto Perfilamiento: Aumentar la frecuencia de compra", style= {"margin-left":"10rem"}),
        dbc.Row(
            dbc.Col(                
                html.P("Se busca aumentar la frecuencia de compra anual por encima de 1.5 comrpas al año por cliente, \
                        a través de un perfilamiento del cliente que permita recomendaciones que generen nuevos momentos\
                        de compra durante el año.")
            ), className="m-3"
        ),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Exploración"),
                        html.P(
                            "Análisis de indicadores generales a través del tiempo:"),
                        html.P("Frecuencia"),
                        html.P("Ventas en el tiempo"),
                        html.P("Geolocalización"),
                        dbc.Button("IR >>", color="dark", id="button-kpi")
                    ])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Perfilamiento"),
                        html.P(
                            "Resultado de los perfiles del cliente y sus carácterísticas"),
                        dbc.Button("IR >>", color="dark",
                                   id="button-cluster")
                    ]),
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Recomendación"),
                        html.P(
                            "Productos y hábitos de compra asociados a cada perfil"),
                        dbc.Button("IR >>", color="dark",
                                   id="button-result")
                    ])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("XXI"),
                        html.P(
                            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. \
                        Aenean euismod euismod tempus. Proin lobortis, nunc auctor \
                        commodo sollicitudin, leo quam."),
                        dbc.Button("IR >>", color="dark", id="button-xxi")
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
            html.H4("Menú", className = "lead navbar-brand", style = {"margin-left":"2rem"}),  
            html.Hr(),  # Esto es una línea horizontal que separa lo de arriba
            html.Div(
                [
                    dbc.Button("Inicio", id="link-hoja-main",
                               style = {"font-size": "12px"},
                               className="btn btn-warning m-1" ),
                    dbc.Button("Exploración", id="link-hoja-1",
                               style = {"font-size": "12px"},
                               className="btn btn-warning m-1"),
                    dbc.Button("Perfilamiento", id="link-hoja-2",
                               style = {"font-size": "12px"},
                               className="btn btn-warning m-1"),
                    dbc.Button("Recomendacion", id="link-hoja-3",
                               style = {"font-size": "12px"},
                               className="btn btn-warning m-1"),
                ],
            ),
        ], style=SIDEBAR_STYLE #,className="navbar navbar-dark bg-dark"
    )
    return sidebar

#-------------------------------------------------------------------------------- Graphs
graphs = html.Div([
    html.H4(["Indicadores de Frecuencia"], style=CONTENT_STYLE_SUBTITLE),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graf6", figure=graf6)
        ]),
        dbc.Col([
            dcc.Graph(id="graf6", figure=graf6) # pendiente gráfica nueva
        ]),
    ]),
    html.H4(["Evolución de ventas"], style=CONTENT_STYLE_SUBTITLE),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                placeholder="Options",
                id="date_dropdown",
                value="year_factura",
                className="dropdown m-3",
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
                className="m-3",
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
            html.Div(
                dcc.Graph(id="graf5", figure=graf5)
            ),
        ]),
        dbc.Col([
            html.Div(
                dcc.Graph(id="graf0", figure=graf0)
            ),
        ]),
    ])
])
