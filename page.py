import os
import dash
import random
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# DATA ORIGINAL
bd = pd.read_csv("data/offcorss_transac_agr_202010102240.csv",
                 sep=";")

# AGRUPACION 1

bd_grupo1 = bd[["year_mes_factura", "trimestre", "year_factura", "tipo_tienda",  "vlr_neto", "qt_facturas_unq", "qt_articulo_unq"]].\
    groupby(["year_mes_factura", "trimestre",
             "year_factura", "tipo_tienda"]).sum()

bd_grupo1 = bd_grupo1.reset_index()
bd_grupo1["vlr_neto_M"] = bd_grupo1["vlr_neto"] / \
    1000000  # Manejar la cifra en millones?
bd_grupo1["ticket_prom"] = bd_grupo1["vlr_neto"] / bd_grupo1["qt_facturas_unq"]

# PROCEDIMIENTO 1 +  GRAFICA 0
# % Crecimiento MoM

para = ["TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]
for t in para:
    deltas = []
    temp = bd_grupo1[bd_grupo1["tipo_tienda"] == t]["vlr_neto"].reset_index()
    for i, e in enumerate(temp["vlr_neto"]):
        meses_ex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        if i in meses_ex:
            a = None
        else:
            a = float((e/temp["vlr_neto"][i-12])-1)
        deltas.append(a)
    deltas = pd.Series(deltas)
    if t == "TIENDA PROPIA":
        deltas_todo = deltas
    else:
        deltas_todo = pd.concat([deltas_todo, deltas], axis=1)
deltas_todo = pd.concat(
    [pd.Series(bd_grupo1["year_mes_factura"].unique()), deltas_todo], axis=1)
deltas_todo = deltas_todo.iloc[12:, ]
deltas_todo.columns = ["fecha", "TP", "TV", "FR"]
# GRAFICA 0: Ingresos month over mont MoM

graf0 = go.Figure(layout=go.Layout(
    autosize=False,
    width=800,
    height=400,
    title='Variaciones MoM por canal')

)
graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["TP"],
                           mode='lines+markers',
                           name='TP'))
graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["TV"],
                           mode='lines+markers',
                           name='TV'))
graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["FR"],
                           mode='lines+markers',
                           name='FR'))


# GRAFICA 1: BAR Ingresos por canal
graf1 = px.bar(bd_grupo1, x="year_mes_factura", y="vlr_neto_M", color="tipo_tienda", width=800, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               category_orders={"tipo_tienda": [
                   "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
               title="Ingresos por canal (Millones COP)")
graf1.update_layout(xaxis_tickangle=90)

# GRAFICA 2: BAR Númeor de ventas por canal
graf2 = px.bar(bd_grupo1, x="year_mes_factura", y="qt_facturas_unq",
               color="tipo_tienda", width=800, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               category_orders={"tipo_tienda": [
                   "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
               title="Número de ventas por canal")
graf2.update_layout(xaxis_tickangle=90)


# GRAFICA 3: PIE Share de ingresos
graf3 = px.pie(bd_grupo1, values='vlr_neto_M', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Ingresos por canal')


# GRAFICA 4:PIE Share de número de ventas
graf4 = px.pie(bd_grupo1, values='qt_facturas_unq', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Número de ventas por canal')


# GRAFICA 5: LINE Evolución ticket promedio
graf5 = px.line(bd_grupo1, x="year_mes_factura", y="ticket_prom",
                color="tipo_tienda", width=800, height=400,
                color_discrete_map={
                    "TIENDA PROPIA": "gold",
                    "TIENDA VIRTUAL": "black",
                    "FRANQUICIAS": "silver"
                },
                category_orders={"tipo_tienda": [
                    "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
                title="Evolución ticket promedio")
graf5.update_layout(xaxis_tickangle=90)

# Components

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.Img(src=app.get_asset_url("offcorss.jpg"), width=150)
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Nav(
                    [
                        dbc.NavLink("Page 1"),
                        dbc.NavLink("Page 2"),
                        dbc.NavLink("Page 3")
                    ],
                    vertical=True,
                    pills=True
                )
            )
        )
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "witdh": "16rem",
        "padding": "2rem 3rem",
        "color": "white",
        "background-color": "black"
    }
)

CONTENT_STYLE = {
    "margin-left": "11rem",
    "margin-right": "auto",
    "padding-top": "10rem",
    "background-color": "#FBD600",
    "position": "absolute"
}

df = pd.DataFrame({
    "Name": ["Example" + str(i + 1) for i in range(100)],
    # Latitude between 4.700100 and 4.710000
    "Latitud": [random.uniform(4.700100, 4.710000) for i in range(100)],
    # Longitude between -74.070100 and -74.080000
    "Longitud": [random.uniform(-74.070100, -74.080000) for i in range(100)],
    "Clientes": [random.randint(0, 100) for i in range(100)],
    "PromedioCompra": [random.uniform(0, 100) for i in range(100)],
})

fig = px.scatter_mapbox(df, lat="Latitud", lon="Longitud", color="PromedioCompra",
                        size="Clientes", mapbox_style="carto-positron", zoom=14.5)

map_graph = dcc.Graph(
    id="map_graph",
    figure=fig
)

graphs = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                ])
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            # One bar graph
        ]),
        dbc.Col([
            # One line raph
        ])
    ]),

    dcc.Graph(id="graf1", figure=graf1),
    dcc.Graph(id="graf3", figure=graf3),
    dcc.Graph(id="graf5", figure=graf5),
    dcc.Graph(id="graf0", figure=graf0),
    map_graph
])

content = html.Div([
    html.Img(src=app.get_asset_url("banner.webp"), style={"width": "1000px", "text-align": "right"}),
    html.Div(style=CONTENT_STYLE), graphs
], style={})

app.layout = html.Div([navbar, content])

if __name__ == "__main__":
    app.run_server(debug=True)
