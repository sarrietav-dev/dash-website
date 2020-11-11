import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Div import Div

from styles import *
from graphs import *
from model import *


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
        html.H3("Seguimiento a la Frecuencia", style={"margin-left": "20rem"}),
        dbc.Row(
            dbc.Col(
                html.P("INTRODUCCIÓN: Offcorss es la empresa lider en el mercado, y como tal busca impactar positivamente\
                        los resultados de negocio por medio de las herramientas analíticas y equipo humano \
                        en alianza con  el programa DS4A.\
                        PROBLEMA: Se desea aumentar la frecuencia de compra anual por encima de 1.5 compras al año por cliente, \
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
                        html.P("Frecuencia, ventas en el tiempo, geolocalización"),
                        dbc.Button("IR", color="dark", id="button-kpi")
                    ])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Perfilamiento"),
                        html.P(
                            "Resultado de los perfiles del cliente y sus carácterísticas"),
                        dbc.Button("IR", color="dark",
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
                        dbc.Button("IR", color="dark",
                                   id="button-result")
                    ])
                ], color="warning", outline=True)
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Documentación"),
                        html.P(
                            "Glosario  y conceptos.\
                            Vínculos a documentación del aplicativo."),
                        dbc.Button("IR", color="dark", id="button-xxi")
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
            html.H4("Menú", className="lead navbar-brand",
                    style={"margin-left": "2rem"}),
            html.Hr(),  # Esto es una línea horizontal que separa lo de arriba
            html.Div(
                [

                    dbc.Button("Inicio", id="link-hoja-main",
                               style={"font-size": "12px"},
                               className="btn btn-warning m-1"),
                    dbc.Button("Exploración", id="link-hoja-1",
                               style={"font-size": "12px"},
                               className="btn btn-warning m-1"),
                    dbc.Button("Perfilamiento ", id="link-hoja-2",
                               style={"font-size": "12px"},
                               className="btn btn-warning m-1"),
                    dbc.Button("Recomendaciones", id="link-hoja-3",
                               style={"font-size": "10px"},
                               className="btn btn-warning m-1"),
                ],
            ),
        ], style=SIDEBAR_STYLE  # ,className="navbar navbar-dark bg-dark"
    )
    return sidebar


# -------------------------------------------------------------------------------- Graphs PAG1
graphs_tab2 = html.Div([
    html.H4(["Indicadores de Frecuencia"], style=CONTENT_STYLE_SUBTITLE),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graf6", figure=graf6)
        ]),
        dbc.Col([
            dcc.Graph(id="graf7", figure=graf7)
        ], style={"margin-left": "1rem"}),
    ]),
    ])
    


graphs_tab1 = html.Div([
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


# -------------------------------------------------------------------------------- Graphs PAG2

dropdown2 = dcc.Dropdown(
    placeholder="Options",
    id="clu_dropdown_x",
    value="recencia_meses",
    className="dropdown m-3",
    options=[
        {"label": "Revenue", "value": "revenue"},
        {"label": "Recencia", "value": "recencia_meses"},
        {"label": "Visitas", "value": "visitas"},
        {"label": "Compras", "value": "compras"},
        {"label": "Ticket promedio",
         "value": "ticket_prom_compra"},
        {"label": "Precio promedio compra",
         "value": "precio_promedio"},
        {"label": "Promedio meses talla", "value": "avg_meses"},
        {"label": "Rango meses tallas compradas",
         "value": "ran_meses"},
    ]
)

dropdown3 = dcc.Dropdown(
    placeholder="Options",
    id="clu_dropdown_y",
    value="revenue",
    className="dropdown m-3",
    options=[
        {"label": "Revenue", "value": "revenue"},
        {"label": "Recencia", "value": "recencia_meses"},
        {"label": "Visitas", "value": "visitas"},
        {"label": "Compras", "value": "compras"},
        {"label": "Ticket promedio",
         "value": "ticket_prom_compra"},
        {"label": "Precio promedio compra",
         "value": "precio_promedio"},
        {"label": "Promedio meses talla", "value": "avg_meses"},
        {"label": "Rango meses tallas compradas",
         "value": "ran_meses"},
    ]
)

# Dropdown para filtrar lineplot de tiendas
dropdown4_1 = dcc.Dropdown(
    placeholder="Options",
    id="dropdown41_año",
    value=[],
    className="dropdown m-3",
    options=[
        {"label":i, "value":i} for i in bd_frec_tienda2["yeard"].unique()
    ],
    searchable = False
)


dropdown5_1 = dcc.Dropdown(
    placeholder="Options",
    id="dropdown51_canal",
    value="TIENDA PROPIA",
    className="dropdown m-3",
    options=[
        {"label":i, "value":i} for i in bd_frec_tienda2["tipo_tienda"].unique()
    ],
    searchable = False
)


# Dropdown with no values
dropdown6_1 = dcc.Dropdown( 
    placeholder="Options",
    id="dropdown61_tienda",
    value=[],
    className="dropdown m-3",
    searchable = False
    
)


input_recencia = dcc.Input(
    id="input_recencia",
    type="number",
    placeholder="recencia en meses",
    value=25
)

slider_ticket = dcc.RangeSlider(
    id="slider-ticket",
    min=df_cluster2["ticket_prom_compra"].min(),
    max=df_cluster2["ticket_prom_compra"].max(),
    marks={df_cluster2["ticket_prom_compra"].min():  "mínimo ticket",
           df_cluster2["ticket_prom_compra"].max():  "máximo ticket"
           },
    value=[90000, 150000]
)


graphs2 = html.Div([
    html.H4(["Medidas de los clústeres"], style=CONTENT_STYLE_SUBTITLE),
    dbc.Row([
        dbc.Col([
                dcc.Graph(id="mg5", figure=mg5)
                ]),
        dbc.Col([
                dcc.Graph(id="mg2", figure=mg2)
                ]),
    ]),
    html.H4(["Contenido clústeres"], style=CONTENT_STYLE_SUBTITLE),
    dbc.Row([
        dbc.Col([
                html.P("Selección variable eje X:"),
                dropdown2,
                html.P("Selección variable eje Y:"),
                dropdown3,
                html.P("Ingrese valor límite de recencia en meses:"),
                input_recencia,
                slider_ticket,
                ], style={"margin-left": "5rem"}),
        dbc.Col([
                dcc.Graph(id="mg3", figure=mg3)
                ]),
    ]),

    dbc.Row([
        dbc.Col([
                dcc.Graph(id="mg4", figure=mg4)
                ]),
    ])
])

perfilamiento_header = html.Div([
    dbc.Row([
        html.Div([
            dbc.Col(dbc.Button("Button1", color="secondary", id="perf_button1")),
            dbc.Col(dbc.Button("Button2", color="secondary", id="perf_button2")),
            dbc.Col(dbc.Button("Button3", color="secondary", id="perf_button3")),
        ], style={"display": "flex", "justify-content": "center"}),
    ]),
    dbc.Row(
        html.Div(
            dbc.Col(
                html.P("", id="perf_paragraph")
            ), style={"display": "flex", "justify-content": "center"}
        ),
    )
], style={"margin": "0 auto"})

content2 = html.Div([
    html.H1(["Perfilamiento"], style=CONTENT_STYLE),
    html.Div(
        [dbc.Row(dbc.Col(html.H5("Seleccione un clúster para ver sus estadísticas:")))
         ], style={}),
    perfilamiento_header,
    graphs2
], style={"margin-left": "10rem"})
