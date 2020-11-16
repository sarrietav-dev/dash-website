import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from graphs import *
from styles import *
from layouts import *
from model import *
from result import *

app = dash.Dash(external_stylesheets=[
                dbc.themes.LUX], suppress_callback_exceptions=True)


##################################################################################################################################
############################################################## CONTENIDO #########################################################
##################################################################################################################################

# ____________________________________________CONTENIDO HOJA 1 ___________________________________________________________________

resumen = html.Div([
    html.H1(["Offcorss Dash Frecuencia"], style=CONTENT_STYLE),
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
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="graf9", figure=graf9)
            ], align="center", width=9),
        ]),
    ], style={"display": "flex", "justify-content": "center"}),
    dbc.Row([
        dbc.Col([
            dropdown4_1,
            dropdown5_1,
            dropdown6_1,
            dbc.Button("Borrar", color="Primary", id="boton_borrar"),
        ], width=4),

        dbc.Col([
            dcc.Graph(id="graf8", figure=graf8)
        ]),
    ]),

], style={"margin-left": "10rem"})

#----------------------------------------------------------------------------------------------------------- Tabs

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'cornsilk',
    'color': 'black',
    'padding': '6px'
}


tabs = dcc.Tabs(
    children=[
        dcc.Tab(tab1_content, label="Contexto", style=tab_style,
                selected_style=tab_selected_style),
        dcc.Tab(tab2_content, label="Frecuencia", style=tab_style,
                selected_style=tab_selected_style),

    ],
)

# ___________________________________________ CONTENIDO HOJA 2 ___________________________________________________________________
# Ver hoja layout línea 387

# ___________________________________________ CONTENIDO HOJA 3 ___________________________________________________________________
content3 = html.Div([
    html.H1(["RECOMENDACIONES"], style=CONTENT_STYLE),
    html.P("Vet el top 10 de productos y su detalle. \
            Elegir primero una categoria de edad masculina o femenina, y luego el clúster deseado."),
    dbc.Row([
        dbc.Col([
                html.Div([
                    html.Img(src=app.get_asset_url('niños_03.jpg'),
                             style={"height": "50%", "width": "23%"}),
                    dbc.Button("Primi", size="lg", className="m-2",
                               color="warning",  id="primi_m"),
                    dbc.Button("Bebe", size="lg", className="m-2",
                               color="warning", id="bebe_m"),
                    dbc.Button("Niño", size="lg", className="m-2",
                               color="warning", id="niño_m")
                ], style={"margin-left": "10rem"})

                ]),

        dbc.Col([
                html.Div([
                         html.Img(src=app.get_asset_url('niñas_03.jpg'),
                                  style={"height": "50%", "width": "15%"}),
                         dbc.Button("Primi", size="lg", className="m-2",
                                    color="warning",  id="primi_f"),
                         dbc.Button("Bebe", size="lg", className="m-2",
                                    color="warning", id="bebe_f"),
                         dbc.Button("Niña", size="lg", className="m-2",
                                    color="warning", id="niño_f")
                         ], style={}
                         ),
                ])
    ]),


    html.Div([
        html.H4(["Productos más populares"], style=CONTENT_STYLE_SUBTITLE)
    ]),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.P("Top 10 / Bottom 5:"),
                dropdown_top,
            ]),
            dbc.Col([
                html.P("Seleccionar clúster:"),
                dropdown_clu,
            ]),
            dbc.Col([
                html.P("Seleccionar producto:"),
                dropdown_prod,
            ]),

        ])
    ]),

    html.Div([
        dbc.Row([
            dbc.Col(
                dcc.Graph(id="rg1", figure=rg1),
            ),
            dbc.Col(
                dcc.Graph(id="rg2", figure=rg2)
            )
        ])
    ]),

], style={"margin-left": "10rem"}
)

# ___________________________________________________ LAYOUT _______________________________________________________________

app.layout = html.Div([
    dcc.Location(id="url"),  # refresh = False
    html.Div(sidebar("none"), style={"display": "none"}),
    main_page(app, True),
    html.Div(content_us(app, False), style={"display": "none"}),
], id="page-content")

hoja_principal = html.Div([
    html.Div(sidebar("none"), style={"display": "none"}),
    main_page(app, True),
    html.Div(content_us(app, False), style={"display": "none"}),
])

hoja_1_layout = html.Div([
    sidebar("block"),
    resumen,
    tabs,
    main_page(app, False),
    html.Div(content_us(app, False), style={"display": "none"}),
    html.Div(id='page-1-content'),
])

hoja_2_layout = html.Div([
    sidebar("block"), content2,
    main_page(app, False),
    html.Div(content_us(app, False), style={"display": "none"}),
])


hoja_3_layout = html.Div([
    sidebar("block"), content3,
    main_page(app, False),
    html.Div(content_us(app, False), style={"display": "none"}),
])

layout_nosotros = html.Div([
    html.Div(sidebar("none"), style={
             "display": "none"}), content_us(app, True),
    main_page(app, False),
])

doc_layout = html.Div([
    sidebar("block"), documentation,
    main_page(app, False),
    html.Div(content_us(app, False), style={"display": "none"}),
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
        Input("link-hoja-4", "n_clicks"),
        Input("button-kpi", "n_clicks"),
        Input("button-cluster", "n_clicks"),
        Input("button-result", "n_clicks"),
        Input("button-doc", "n_clicks"),
        Input("button-us", "n_clicks"),
        Input("back-button", "n_clicks")
    ]
)
def display_page(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "link-hoja-1" in changed_id or "button-kpi" in changed_id:
        return hoja_1_layout
    elif "link-hoja-2" in changed_id or "button-cluster" in changed_id:
        return hoja_2_layout
    elif "link-hoja-3" in changed_id or "button-result" in changed_id:
        return hoja_3_layout
    elif "button-us" in changed_id:
        return layout_nosotros
    elif "button-doc" in changed_id:
        return doc_layout
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


# ------------------------------------------------------------------------------ Callback para el pintar y borrar tienda en graf8

@app.callback(
    Output("graf8", "figure"),
    [Input("dropdown61_tienda", "value"),
     Input("dropdown41_año", "value"), Input("boton_borrar", "n_clicks")]
)
def pinta_tienda1(tienda_1, año_1, n_clicks):
    changed_ids = [p['prop_id'].split('.')[0]
                   for p in dash.callback_context.triggered]
    button_pressed = 'boton_borrar' in changed_ids

    if not button_pressed:

        trace1_df = bd_frec_tienda2[(bd_frec_tienda2["yeard"] == año_1) &
                                    (bd_frec_tienda2["d_centro"] != "TIENDA SAN ANDRES 2") &
                                    (bd_frec_tienda2["d_centro"] == tienda_1)]

        graf8.add_traces(go.Scatter(x=trace1_df["mes"],
                                    y=trace1_df["freq_acum"],
                                    mode='lines+markers',
                                    name=str(año_1) + " " + str(tienda_1),
                                    ),)
        return graf8
    else:
        graf8.update_traces(go.Scatter(x=[],
                                       y=[],
                                       mode='lines+markers',
                                       name="",
                                       line=dict(color="black")),
                            )

        return graf8

# __________________________________________ CALLBACKS HOJA 2 ____________________________________________________________________


@app.callback(
    [Output("mg3", "figure"), Output("mg4", "figure")],
    [Input("clu_dropdown_x", "value"),
     Input("clu_dropdown_y", "value"),
     Input("slider_ticket", "value"),
     Input("slider_recencia", "value"),
     Input("drop_tree", "value"),

     ]
)
def change_par(valor_eje_x, valor_eje_y, ticket, recencia, drop_tree):
    updated_df = df_cluster2[(df_cluster2["recencia_meses"] <= recencia[1]) &
                             (df_cluster2["recencia_meses"] > recencia[0]) &
                             (df_cluster2["ticket_prom_compra"] <= ticket[1]) &
                             (df_cluster2["ticket_prom_compra"] > ticket[0])
                             ]

    mg3 = px.scatter(updated_df,
                     x=valor_eje_x,
                     y=valor_eje_y,
                     color="cluster_name",
                     title='Scatter pares de variables',
                     height=550)

    mg4 = px.treemap(updated_df, path=[px.Constant('CLIENTES:  ' + str(updated_df["constante_cli"].sum())),
                                       "canal_det", 'region', "cluster_name"],
                     values='constante_cli',
                     color=drop_tree,
                     title="Visualizador de clientes: Canal/Región/Clúster: " +
                     "Recencia desde " + "{:.0f}".format(recencia[0]) + " hasta " + "{:.0f}".format(recencia[1]) +
                     " - Ticket desde " +
                     "${:10,.0f}".format(
                         ticket[0]) + " hasta " + "${:10,.0f}".format(ticket[1]),
                     color_continuous_scale='thermal_r',
                     height=700)

    return mg3, mg4


@app.callback(
    Output("tabla_resumen_clu", "children"),
    [Input("perf_button1", "n_clicks"),
     Input("perf_button2", "n_clicks"),
     Input("perf_button3", "n_clicks"),
     Input("perf_button4", "n_clicks"), ]
)
def change_paragraph(btn1, btn2, btn3, btn4):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "perf_button1" in changed_id:
        return tabla_A
    elif "perf_button2" in changed_id:
        return tabla_B
    elif "perf_button3" in changed_id:
        return tabla_C
    elif "perf_button4" in changed_id:
        return tabla_D


# __________________________________________ CALLBACKS HOJA 3 ____________________________________________________________________

@app.callback(
    [Output("rg1", "figure"), Output("rg2", "figure")],
    [Input("dropdown_clu_p3", "value"), Input("dropdown_grupo_p3", "value"),
     Input("primi_m", "n_clicks"), Input("primi_f", "n_clicks"),
     Input("bebe_m", "n_clicks"), Input("bebe_f", "n_clicks"),
     Input("niño_m", "n_clicks"), Input("niño_f", "n_clicks"),
     Input("dropdown_top10_p3", "value")
     ]
)
def clu_sel(cluster, grupo_art, n1, n2, n3, n4, n5, n6, top):
    genero = "MASCULINO"
    edad = "PRIMI"
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if "primi_m" in changed_id:
        genero = "MASCULINO"
        edad = "PRIMI"

    if "primi_f" in changed_id:
        genero = "FEMENINO"
        edad = "PRIMI"
        primi_f = 0

    if "bebe_m" in changed_id:
        genero = "MASCULINO"
        edad = "BEBES"
        bebe_m = 0

    if "bebe_f" in changed_id:
        genero = "FEMENINO"
        edad = "BEBES"
        bebe_f = 0

    if "niño_m" in changed_id:
        genero = "MASCULINO"
        edad = "NIÑOS"
        niño_m = 0

    if "niño_f" in changed_id:
        genero = "FEMENINO"
        edad = "NIÑOS"
        niño_f = 0

    tabla_grupo_art = df_grupo_art[(df_grupo_art["genero"] == genero) &
                                   (df_grupo_art["edad"] == edad) &
                                   (df_grupo_art["clu_name"] == cluster)][["grupo_articulo", "cantidad", "freq_relativa"]]\
        .reset_index(drop=True).sort_values(by="cantidad", ascending=False)

    tabla_tipo_art = df_tipo_art[(df_tipo_art["genero"] == genero) &
                                 (df_tipo_art["edad"] == edad) &
                                 (df_tipo_art["clu_name"] == cluster) &
                                 (df_tipo_art["grupo_articulo"] == grupo_art)][["tipo_articulo", "cantidad", "freq_relativa", "tipo_tejido"]]\
        .reset_index(drop=True).sort_values(by="cantidad", ascending=False)


# --------------Gráfica de barras 1: Grupo artículo

    if top == "tail":
        rg1 = px.bar(tabla_grupo_art.tail(5).sort_values(by="cantidad"), x="cantidad", y="grupo_articulo",
                     title="Bottom 5 productos clúster " + cluster + " " + genero + " " + edad,
                     hover_data=["freq_relativa"],
                     color_discrete_map={
            "": "lightsalmon"
        }
        )

    elif top == "head":
        rg1 = px.bar(tabla_grupo_art.head(10).sort_values(by="cantidad"), x="cantidad", y="grupo_articulo",
                     title="Top 10 productos clúster " + cluster + " " + genero + " " + edad,
                     hover_data=["freq_relativa"],
                     color_discrete_map={
            "": "gold"
        }
        )


# --------------Gráfica de barras 2: Tipo artículo
    rg2 = go.Figure(go.Bar(x=tabla_tipo_art[tabla_tipo_art["tipo_tejido"] == 'TEJIDO PLANO']["cantidad"],
                           y=tabla_tipo_art[tabla_tipo_art["tipo_tejido"]
                                            == 'TEJIDO PLANO']["tipo_articulo"],
                           name='TEJIDO PLANO',
                           orientation='h',
                           marker_color='silver'))
    rg2.add_trace(go.Bar(x=tabla_tipo_art[tabla_tipo_art["tipo_tejido"] == 'TEJIDO PUNTO']["cantidad"],
                         y=tabla_tipo_art[tabla_tipo_art["tipo_tejido"]
                                          == 'TEJIDO PUNTO']["tipo_articulo"],
                         name='TEJIDO PUNTO',
                         orientation='h',
                         marker_color='gold'))
    rg2.add_trace(go.Bar(x=tabla_tipo_art[tabla_tipo_art["tipo_tejido"] == 'NO TEJIDO']["cantidad"],
                         y=tabla_tipo_art[tabla_tipo_art["tipo_tejido"]
                                          == 'NO TEJIDO']["tipo_articulo"],
                         name='NO TEJIDO',
                         orientation='h',
                         marker_color='black'))
    rg2.add_trace(go.Bar(x=tabla_tipo_art[tabla_tipo_art["tipo_tejido"] == 'INDISTINTO']["cantidad"],
                         y=tabla_tipo_art[tabla_tipo_art["tipo_tejido"]
                                          == 'INDISTINTO']["tipo_articulo"],
                         name='INDISTINTO',
                         orientation='h',
                         marker_color='lightsalmon'))

    rg2.update_layout(barmode='stack', yaxis={
                      'categoryorder': 'total ascending'})
    rg2.update_layout(title_text='Top 10 tipos de ' + grupo_art)

    return rg1, rg2


# ______________________________________________________________________________________________________
if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)
