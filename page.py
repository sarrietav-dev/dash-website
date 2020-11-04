import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from graphs import *
from styles import *
from layouts import *
from model import *

app = dash.Dash(external_stylesheets=[
                dbc.themes.LUX], suppress_callback_exceptions=True)


# Dropdown1:
# Este dropdown es para graf1 y graf3, para seleccionar ver en cantidad o rev

dropdown1 = html.Div([
    dbc.DropdownMenu(
        label="Ingresos o productos",
        children=[
            dbc.DropdownMenuItem("Ingresos"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Productos")
        ])
])

#################################################################################################################################
############################################################## CONTENIDO #########################################################


summary = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div("Núm registros:" + '{:10,.0f}'.format(
                bd_unicos.iloc[0, 0]), style={"margin-left": "2rem"}),
            html.Div("Clientes únicos:" + '{:10,.0f}'.format(
                bd_unicos.iloc[0, 2]), style={"margin-left": "2rem"}),
            html.Div("Compras únicas:" + '{:10,.0f}'.format(
                bd_unicos.iloc[0, 1]), style={"margin-left": "2rem"}),
            html.Div("Total Revenue:" + '{:10,.0f}'.format(
                bd_unicos.iloc[0, 4]), style={"margin-left": "2rem"}),
            html.Div(
                "Info desde:" + '{}'.format(bd_unicos.iloc[0, 5]), style={"margin-left": "2rem"}),
            html.Div(
                "Info. hasta" + '{}'.format(bd_unicos.iloc[0, 6]), style={"margin-left": "2rem"})

        ]),
        dbc.Col([
            #html.Div("Info desde:" + '{}'.format(bd_unicos.iloc[0, 5]), style={"margin-right": "10rem"}),
            #html.Div("Info. hasta" +'{}'.format(bd_unicos.iloc[0, 6]), style={})
        ]),
    ]),
])

# ------------------------------------------------------------------ Content PAG1
content = html.Div([
    html.H1(["Offcorss Dash mock-up"], style=CONTENT_STYLE),
    html.Div(
        [dbc.Row(dbc.Col(html.H5("Resumen de la base:")))
         ], style={}),
    tabla1,
    html.P(["Información desde >>>> " + bd_unicos.iloc[:, 5]
            [0] + "  hasta >>>> " + bd_unicos.iloc[:, 6][0]]),
    graphs,
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
    html.Div(id="prueba"),
], style={"margin-left": "10rem"})


# ------------------------------------------------------------------ Content PAG2


#dcc.Graph(id = "mg1", figure = mg1)


#------------------------------------------------------------------- Layout
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
    sidebar(True), content,
    main_page(app, False),
    html.Div(id='page-1-content')
])

hoja_2_layout = html.Div([
    sidebar(True), content2,
    main_page(app, False),
    html.Div(id='page-2-content')

])


################################################################################################################################
####################################################### INTERACTIVIDAD #########################################################
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


# ------------------------------------------------------------------------- Callback para cambiar tiempo de  graf5
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


# __________________________________________ CALLBACKS HOJA 2 ______________________________________________

@app.callback(
    [Output("mg3", "figure"), Output("mg4", "figure")],
    [Input("clu_dropdown_x", "value"), Input(
        "clu_dropdown_y", "value"), Input("input_recencia", "value")]
)
def change_par(valor_eje_x, valor_eje_y, vals):

    updated_df = df3_mod[df3_mod["recencia_meses"] <= vals]

    mg3 = px.scatter(updated_df,
                     x=valor_eje_x,
                     y=valor_eje_y,
                     color="clusters",
                     title='Scatter pares de variables')

    mg4 = px.treemap(updated_df, path=[px.Constant('CLIENTES:  ' + str(updated_df["constante_cli"].sum())),
                                       "canal_det", 'region', "ciudad", "clusters"],
                     values='constante_cli',
                     color='recencia_meses',
                     title="Visualizador de clientes",
                     color_continuous_scale='thermal_r',
                     height=700)

    return mg3, mg4


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
