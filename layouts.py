from dash_bootstrap_components._components.CardDeck import CardDeck
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
        html.H3("Seguimiento a la Frecuencia", style={"text-align": "center"}),
        dbc.Row(
            dbc.Col(
                html.P("INTRODUCCIÓN: Offcorss es la empresa lider en el mercado, y como tal busca impactar positivamente\
                        los resultados de negocio por medio de las herramientas analíticas y equipo humano \
                        en alianza con  el programa DS4A.\
                        PROBLEMA: Se desea aumentar la frecuencia de compra anual por encima de 1.5 compras al año por cliente, \
                        a través de un perfilamiento del cliente que permita recomendaciones que generen nuevos momentos\
                        de compra durante el año.")
            ), className="m-3", justify="center"),
        dbc.CardDeck([

            dbc.Card([
                dbc.CardBody([
                    html.H4("Exploración"),
                    html.P(
                        "Análisis de indicadores generales a través del tiempo:"),
                    html.P("Frecuencia, ventas en el tiempo, geolocalización"),
                    dbc.Button("IR", color="dark", id="button-kpi")
                ])
            ], color="warning", outline=True),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Segmentación"),
                    html.P(
                        "Resultado de los segmentos del cliente para toda la base y sus carácterísticas"),
                    dbc.Button("IR", color="dark",
                               id="button-cluster")
                ]),
            ], color="warning", outline=True),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Recomendación"),
                    html.P(
                        "Prendas asociados a cada segmento de cliente"),
                    dbc.Button("IR", color="dark",
                               id="button-result")
                ])
            ], color="warning", outline=True),
            dbc.Card([
                dbc.CardBody([
                    html.H4("Documentación"),
                    html.P(
                        "Glosario  y conceptos.\
                            Vínculos a documentación del aplicativo."),
                    dbc.Button("IR", color="dark", id="button-doc")
                ])
            ], color="warning", outline=True),
        ]),
        dbc.Row(
            dbc.Col(
                html.Div(
                    dbc.Button("Nosotros", id="button-us", color="info", className="m-4"), style={"display": "flex", "justify-content": "center", "align-items": "center"}),
            )
        )
    ], style={"display": "block" if visible else "none", "background-color": "#efe8df"})

    return main_page


def sidebar(visible_nav):
    SIDEBAR_STYLE["display"] = visible_nav
    sidebar = html.Nav(
        [
            html.H4("Menú", className="lead navbar-brand",
                    style={"margin-left": "2rem"}),
            html.Hr(),  # Esto es una línea horizontal que separa lo de arriba
            html.Div([

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
                dbc.Button("Documentación", id="link-hoja-4",
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


# Dropdown para filtrar lineplot de tiendas
dropdown4_1 = dcc.Dropdown(
    placeholder="Options",
    id="dropdown41_año",
    value=[],
    className="dropdown m-3",
    options=[
        {"label": i, "value": i} for i in bd_frec_tienda2["yeard"].unique()
    ],
    searchable=False
)


dropdown5_1 = dcc.Dropdown(
    placeholder="Options",
    id="dropdown51_canal",
    value="TIENDA PROPIA",
    className="dropdown m-3",
    options=[
        {"label": i, "value": i} for i in bd_frec_tienda2["tipo_tienda"].unique()
    ],
    searchable=False
)


# Dropdown with no values
dropdown6_1 = dcc.Dropdown(
    placeholder="Options",
    id="dropdown61_tienda",
    value=[],
    className="dropdown m-3",
    searchable=False

)


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


# input_recencia = dcc.Input(
# id="input_recencia",
# type="number",
##    placeholder="recencia en meses",
# value=25
# )

# ------------------------------------------------------------------ Slider ticket promedio
slider_ticket = dcc.RangeSlider(
    id="slider_ticket",
    min=df_cluster2["ticket_prom_compra"].min(),
    max=df_cluster2["ticket_prom_compra"].max(),
    marks={df_cluster2["ticket_prom_compra"].min(): "mín",
           50000: "25k",
           100000: "50k",
           200000: "200k",
           300000: "300k",
           400000: "400k",
           600000: "600k",
           1000000: "1M",
           df_cluster2["ticket_prom_compra"].max():  "máx"
           },
    step=50000,
    value=[df_cluster2["ticket_prom_compra"].min(
    ), df_cluster2["ticket_prom_compra"].max()]
)

# ------------------------------------------------------------------- Slider recencia
slider_recencia = dcc.RangeSlider(
    id="slider_recencia",
    min=df_cluster2["recencia_meses"].min(),
    max=df_cluster2["recencia_meses"].max(),
    marks={df_cluster2["recencia_meses"].min():  "mín",
           3: "3meses",
           6: "6meses",
           9: "9meses",
           12: "12meses",
           18: "16meses",
           24: "24meses",
           df_cluster2["recencia_meses"].max():  "máx"
           },
    step=1,
    value=[df_cluster2["recencia_meses"].min(
    ), df_cluster2["recencia_meses"].max()]
)

# ---------------------------------------------------------------Dropdown escala color treemap
dropdow_escala_tree = dcc.Dropdown(
    placeholder="Options",
    id="drop_tree",
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

# --------------------------------------------------------------------------------------------------------Elemento graphs2

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
                html.Div([html.P("Selección variable eje X:")],
                         style={"margin-top": "1rem"}),
                dropdown2,
                html.P("Selección variable eje Y:"),
                dropdown3,
                html.P("Seleccione el rango de ticket promedio (step 50k):"),
                html.Div(slider_ticket, style={"margin-bottom": "3.5rem"}),
                html.P("Seleccione el rango de recencia en meses:"),
                html.Div(slider_recencia, style={"margin-bottom": "3.5rem"}),
                html.Div([html.P("Selección escala de color:")],
                         style={"margin-top": "1rem"}),
                dropdow_escala_tree,
                ], style={"margin-left": "5rem"}),
        dbc.Col([
                dcc.Graph(id="mg3", figure=mg3)
                ]),
    ]),

    dbc.Row([
        dbc.Col([
                dcc.Graph(id="mg4", figure=mg4)
                ])
    ]),
    html.P("OU: Outlet, TP: Tienda propia, FR: Franquicia\
        El tamaño de cada cuadrado indica el número de clientes."),
])

# ---------------------------------------------------------------------- Botones segmento
perfilamiento_header = html.Div([
    dbc.Row([
        html.Div([
            dbc.Col(dbc.Button("Sale hunters", color="warning",
                               id="perf_button1", size="sm")),
            dbc.Col(dbc.Button("Average customer", color="warning",
                               id="perf_button2", size="sm")),
            dbc.Col(dbc.Button("Selective customer",
                               color="warning", id="perf_button3", size="sm")),
            dbc.Col(dbc.Button("Offcorss fanatics",
                               color="warning", id="perf_button4", size="sm")),

        ], style={"display": "flex", "justify-content": "center"}),
    ]),
    dbc.Row(
        html.Div(
            dbc.Col(
                html.P("", id="perf_paragraph"),
            ), style={"display": "flex", "justify-content": "center"}
        ),
    )
], style={"margin-left": "15rem"})


# ----------------------------------------------------------------------- Content 2
content2 = html.Div([
    html.H1(["Perfilamiento"], style=CONTENT_STYLE),
    html.Div(
        [dbc.Row(dbc.Col(html.H5("Seleccione un clúster para ver sus estadísticas:"))),
         perfilamiento_header,
         html.Div(id="tabla_resumen_clu")
         ], style={}
    ),
    graphs2
], style={"margin-left": "10rem"})


def content_us(app, visible):
    return html.Div([
        dbc.Row(
            dbc.Col(
                dbc.Button("< Back", color="primary",
                           id="back-button", style={"align-self": "initial"}, className="btn btn-primary m-2")
            )
        ),
        html.Div([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Img(src=app.get_asset_url("team84.jpg"), style={
                            "height": "auto", "max-width": "100%", "width": "25%"})
                    ], style={"display": "flex", "justify-content": "center", "align-items": "center"})  # TODO: Center image
                )]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        # TODO: Center this and make this blue.
                        html.H1("Team 84", style={"color": "#7aa6c0"})
                    ])
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                    ])
                ]),
            ]),
            team_faces(app),
            html.Div(style={"margin": "3em auto"}),
            html.Div(
                dbc.Row(
                    corp_images(app), justify="between"), className="mt-4"
            ),
        ], style={
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "center",
            "min-height": "100%",
            "margin": "0"})
    ], style={
        "background-color": "black",
        "display": "block" if visible else "none"
    })


faces_style = {
    "max-width": "100%",
    "height": "auto",
    "width": "200px",
    "border-radius": "50%",
}


def team_faces(app):
    return dbc.CardDeck([
        dbc.Card([
            dbc.CardImg(src=app.get_asset_url("jenny.jpeg"), top=True),
            dbc.CardBody([
                html.H4("Jeniffer Duarte", className="card-title"),
                html.P("PhD en Estadística", className="card-text"),
                dbc.Button("LinkedIn", color="primary",
                           href="https://www.linkedin.com/in/jeniffer-johana-duarte-sanchez-56317250/", target="_blank")
            ])
        ]),
        dbc.Card([
            dbc.CardImg(src=app.get_asset_url("lau.jpeg"), top=True),
            dbc.CardBody([
                html.H4("Laura Sierra", className="card-title"),
                html.P("Ingeniera Industrial", className="card-text"),
                dbc.Button("LinkedIn", color="primary",
                           href="http://linkedin.com/in/laura-sierra-serna-74413143", target="_blank")
            ])
        ]),
        dbc.Card([
            dbc.CardImg(src=app.get_asset_url("jhonathan.jpeg"), top=True),
            dbc.CardBody([
                html.H4("Jonathan Madrid", className="card-title"),
                html.P("Ingeniero de Sistemas", className="card-text"),
                dbc.Button("LinkedIn", color="primary",
                           href="https://www.linkedin.com/in/jonathan-madrid-hincapie-72015926/", target="_blank")
            ])
        ]),
        dbc.Card([
            dbc.CardImg(src=app.get_asset_url("seb.png"), top=True),
            dbc.CardBody([
                html.H4("Sebastian Arrieta", className="card-title"),
                html.P("Estudiante de Ingeniería de Sistemas",
                       className="card-text"),
                dbc.Button("Github", color="primary",
                           href="https://github.com/sarrietav-dev", target="_blank")
            ])
        ]),
        dbc.Card([
            dbc.CardImg(src=app.get_asset_url("john.jpeg"), top=True),
            dbc.CardBody([
                html.H4("John Davinson", className="card-title"),
                html.P("Administrador de Empresas", className="card-text"),
                dbc.Button("LinkedIn", color="primary",
                           href="https://www.linkedin.com/in/john-davison-a0212022", target="_blank")
            ])
        ]),
    ])


def corp_images(app):
    img_styles = {
        "max-width": "100%",
        "width": "300px",
        "height": "auto",
        "margin": "auto 3em",
    }
    return [
        dbc.Col(
            html.Img(src=app.get_asset_url("corr1.jpeg"), style=img_styles)
        ),
        dbc.Col(
            html.Img(src=app.get_asset_url("ds4a.jpeg"), style=img_styles)
        ),
        dbc.Col(
            html.Img(src=app.get_asset_url("softbank.jpeg"), style=img_styles)
        ),
    ]


documentation = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Visitas"),
            html.P(
                "Catidad de veces que el cliente compró en el periodo de tiempo suministrado.")
        ]),
        dbc.Col([
            html.H2("Frecuencia"),
            html.P(
                "Indicador con medición anual. (Total visitas/ total clientes) en el periodo en cuestión")
        ]),
        dbc.Col([
            html.H2("Ticket Promedio"),
            html.P("Medida en COP. Es el valor promedio de cada compra. Promedio de las sumas de los valores netos de compra    ")
        ]),
    ], className="mb-6"),
    dbc.Row([
        dbc.Col([
            html.H2("Revenue"),
            html.P("Suma del valor neto de las compras.")
        ]),
        dbc.Col([
            html.H2("Edad promedio (Avg age)"),
            html.P("Se definió una variable de edad asociada a la talla comprada, y posteriormente se sacó el promedio de edades para las compras de cada cliente.")
        ]),
        dbc.Col([
            html.H2("Rango edad  (Ran age)"),
            html.P("Basado en el indicador \"avg age\", es el rango entre la máxima edad y la mínima edad para las compras de un cliente. Un rango amplio indica que el cliente compró productos para diversos rangos de edad.")
        ]),
    ])
], style={"margin-left": "10rem"})
