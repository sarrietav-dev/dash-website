import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from graphs import *
from styles import *
from layouts import *
from model import *
from result import *

app = dash.Dash(external_stylesheets=[
                dbc.themes.LUX], suppress_callback_exceptions=True)


### Dropdown1: BORRAR
### Este dropdown es para graf1 y graf3, para seleccionar ver en cantidad o rev
##
##dropdown1 = html.Div([
##    dbc.DropdownMenu(
##        label="Ingresos o productos",
##        children=[
##            dbc.DropdownMenuItem("Ingresos"),
##            dbc.DropdownMenuItem(divider=True),
##            dbc.DropdownMenuItem("Productos")
##        ])
##])

#################################################################################################################################
############################################################## CONTENIDO #########################################################

# ------------------------------------------------------------------ Content PAG1


resumen = html.Div([
    html.H1(["Offcorss Dash mock-up"], style=CONTENT_STYLE),
    html.Div(
        [dbc.Row(dbc.Col(html.H5("Resumen de la base:")))
         ], style={}),
    tabla1,
    html.P(["Información desde >>>> " + bd_unicos.iloc[:, 5]
            [0] + "  hasta >>>> " + bd_unicos.iloc[:, 6][0]])
], style={"margin-left": "10rem"})


tab1_content = html.Div([
    graphs_tab1,
    html.Div(id="prueba"),
], style={"margin-left": "10rem"}
)


tab2_content = html.Div([
    graphs_tab2,
    html.Div([
        html.H4(["Geolocalización tiendas"], style=CONTENT_STYLE_SUBTITLE),
        dbc.Row(
            dbc.Col(
                html.Div([
                    dbc.RadioItems(
                        id="map_radio_items",
                        value="frecuencia",
                        className="m-3",
                        options=[
                            {"label": "frecuencia", "value": "frecuencia"},
                            {"label": "revenues", "value": "revenues"}
                        ])
                ], style={"display": "flex", "justify-content": "center"})
            )
        ),
        dbc.Row([
            dbc.Col([
                html.Div([html.H5("Frecuencia tiendas físicas")],
                         style={"margin-left": "5rem"}),
                map_graph1
            ]),
            dbc.Col([
                html.Div([html.H5("Frecuencia tiendas virtuales")],
                         style={"margin-left": "5rem"}),
                map_graph2
            ]),
        ])
    ]),
    html.H4(["Comparador de frecuencia por tienda"],
            style=CONTENT_STYLE_SUBTITLE),
    dbc.Row([
            dcc.Graph(id="graf9", figure=graf9)
            ], style={"margin-left": "auto"}
            ),
    dbc.Row([
        dbc.Col([
            dropdown4_1,
            dropdown5_1,
            dropdown6_1,
            dbc.Button("Borrar", color="Secondary", id="boton_borrar"),
        ], width=4),

        dbc.Col([
            dcc.Graph(id="graf8", figure=graf8)
        ]),
    ]),

], style={"margin-left": "10rem"})

# ----------------------------------------------------------------------------------------------------------- Tabs

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Contexto",
                tab_style={"margin-left": "auto"}),
        dbc.Tab(tab2_content, label="Frecuencia",
                tab_style={"color": "#00AEF9"})
    ]
)

# -------------------------------------------------------------------------------------------------------- Content PAG2


# ------------------------------------------------------------------- Layout
app.layout = html.Div([
    dcc.Location(id="url"),  # refresh = False
    html.Div(sidebar(False), style={"display": "none"}),
    main_page(app, True),
], id="page-content")

hoja_principal = html.Div([
    html.Div(sidebar(False), style={"display": "none"}),
    main_page(app, True)
])

hoja_1_layout = html.Div([
    sidebar(True),
    resumen,
    tabs,
    main_page(app, False),
    html.Div(id='page-1-content')
])

hoja_2_layout = html.Div([
    sidebar(True), content2,
    main_page(app, False),
    html.Div(id='page-2-content')

])


hoja_3_layout = html.Div([
    sidebar(True), content3,
    main_page(app, False),
    html.Div(id='page-3-content')

])


################################################################################################################################
#########################################         INTERACTIVIDAD       #########################################################
################################################################################################################################

@app.callback(
    [Output(f"link_hoja_{i}", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def habilitar_link(pathname):
    if pathname == "/":
        return True, False, False
    return [pathname == f"/hoja-{i}" for i in range(1, 4)]


@app.callback(
    Output("page-content", "children"),
    [
        Input("link-hoja-main", "n_clicks"),
        Input("link-hoja-1", "n_clicks"),
        Input("link-hoja-2", "n_clicks"),
        Input("link-hoja-3", "n_clicks"),
        Input("button-kpi", "n_clicks"),
        Input("button-cluster", "n_clicks"),
        Input("button-result", "n_clicks"),
        Input("button-xxi", "n_clicks"),
    ]
)
def display_page(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "link-hoja-1" in changed_id or "button-kpi" in changed_id:
        return hoja_1_layout
    elif "link-hoja-2" in changed_id or "button-cluster" in changed_id:
        return hoja_2_layout
    elif "link-hoja-3" in changed_id or "button-result" in changed_id:
        return hoja_3_layout
    else:
        return hoja_principal

# ------------------------------------------------------------------------- Callback para cambiar graf con tiempo, y entre $ y Qt


@app.callback(
    [Output("graf1", "figure"), Output("graf3", "figure")],
    [Input("date_dropdown", "value"), Input("radio_items", "value")]
)
def foo(drop, radio):
    graf1 = px.bar(bd_agr_month, x=drop, y=radio, color="tipo_tienda", width=800, height=400,
                   color_discrete_map={
                       "TIENDA PROPIA": "gold",
                       "TIENDA VIRTUAL": "black",
                       "FRANQUICIAS": "silver"
                   },
                   category_orders={"tipo_tienda": [
                       "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
                   title="Ingresos por canal (Millones COP)")
    graf1.update_layout(xaxis_tickangle=90)

# GRAFICA 3: PIE Share de ingresos
    graf3 = px.pie(bd_agr_month, values=radio, names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
                   color_discrete_map={
                       "TIENDA PROPIA": "gold",
                       "TIENDA VIRTUAL": "black",
                       "FRANQUICIAS": "silver"
                   },
                   title='%Ingresos por canal')

    return graf1, graf3


@app.callback([
    Output("map_graph1", "figure"), Output("map_graph2", "figure")
], Input("map_radio_items", "value"))
def change_map(radio):
    map1 = px.scatter_mapbox(centro_region_agr_2019_TP, lat="latitud_c", lon="longitud_c", color=radio,
                             size="visitas", mapbox_style="carto-positron",
                             height=700, width=600, zoom=4.5)

    map2 = px.scatter_mapbox(centro_region_agr_2019_TV, lat="latitud_m", lon="longitud_m", color=radio,
                             size="visitas", mapbox_style="carto-positron",
                             height=700, width=600, zoom=4.5)

    return map1, map2


# ---------------------------------------------------------------------------------------- Callback para cambiar tiempo de  graf5
@app.callback(
    Output("graf5", "figure"),
    Input("date_dropdown", "value")
)
def prueba(valor):
    if valor == "trim_año":
        return graf5_1
    elif valor == "year":
        return graf5_2
    else:
        return graf5


# --------------------------------------------------------------------------------- Callback para el dropdown tienda de la graf8

@app.callback(
    Output("dropdown61_tienda", "options"),
    Input("dropdown51_canal", "value")
)
def selector_tienda(canal1):
    if canal1 == "TIENDA PROPIA":
        return[{"label": i, "value": i} for i in
               bd_frec_tienda2[bd_frec_tienda2["tipo_tienda"] == canal1]["d_centro"].sort_values().unique()]

    elif canal1 == "FRANQUICIAS":
        return [{"label": i, "value": i} for i in
                bd_frec_tienda2[bd_frec_tienda2["tipo_tienda"] == canal1]["d_centro"].sort_values().unique()]
    else:
        return [{"label": i, "value": i} for i in
                bd_frec_tienda2[bd_frec_tienda2["tipo_tienda"] == canal1]["d_centro"].sort_values().unique()]


# --------------------------------------------------------------------------------- Callback para el pintar la tienda en graf9

@app.callback(
    Output("graf8", "figure"),
    [Input("dropdown61_tienda", "value"), Input(
        "dropdown41_año", "value"), Input("boton_borrar", "n_clicks")]
)
def pinta_tienda1(tienda_1, año_1, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    graf8 = go.Figure(layout=layout)
    if "boton_borrar" in changed_id:
        graf8.update_traces()
        graf8.add_trace(go.Scatter(x=[],
                                   y=[],
                                   mode='lines+markers',
                                   line=dict(color="yellow")
                                   ))
        return graf8
    else:
        trace1_df = bd_frec_tienda2[(bd_frec_tienda2["yeard"] == año_1) &
                                    (bd_frec_tienda2["d_centro"] != "TIENDA SAN ANDRES 2") &
                                    (bd_frec_tienda2["d_centro"] == tienda_1)]

        graf8.add_traces(go.Scatter(x=trace1_df["mes"],
                                    y=trace1_df["freq_acum"],
                                    mode='lines+markers',
                                    name=str(año_1) + " " + str(tienda_1),
                                    ),)
        graf8.update_traces()

        return graf8

# __________________________________________ CALLBACKS HOJA 2 ____________________________________________________________________


@app.callback(
    [Output("mg3", "figure"), Output("mg4", "figure"),
     Output("range", "children")],
    [Input("clu_dropdown_x", "value"), Input(
        "clu_dropdown_y", "value"), Input("slider-ticket", "value")]
)
def change_par(valor_eje_x, valor_eje_y, vals):
    updated_df = df_cluster2[df_cluster2["recencia_meses"] <= vals]


    mg3 = px.scatter(updated_df,
                     x=valor_eje_x,
                     y=valor_eje_y,
                     color="cluster_name",
                     title='Scatter pares de variables')

    mg4 = px.treemap(updated_df, path=[px.Constant('CLIENTES:  ' + str(updated_df["constante_cli"].sum())),
                                       "canal_det", 'region', "cluster_name"],
                     values='constante_cli',
                     color='recencia_meses',
                     title="Visualizador de clientes: Canal/Región/Clúster",
                     color_continuous_scale='thermal_r',
                     height=700)

    return mg3, mg4, "{}".format(vals)


@app.callback(
    [Output("perf_paragraph", "children")],
    [Input("perf_button1", "n_clicks"),
     Input("perf_button2", "n_clicks"),
     Input("perf_button3", "n_clicks"), ]
)
def change_paragraph(btn1, btn2, btn3):
    if btn1 is not None:
        return ["You clicked the 1st button"]
    elif btn2 is not None:
        return ["You clicked the 2st button"]
    elif btn3 is not None:
        return ["You clicked the 3st button"]


# ______________________________________________________________________________________________________
if __name__ == "__main__":
    app.run_server(debug=True)
