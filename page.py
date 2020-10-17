import os
import dash
import random
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from graphs import *
from styles import *
from layouts import main_page, sidebar

app = dash.Dash(external_stylesheets=[
                dbc.themes.LUX], suppress_callback_exceptions=True)


# Esto es data de ejemplo para colocar en el mapa:
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

# Aca van todas la gráficas:
graphs = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graf1", figure=graf1)
        ]),
        dbc.Col([
            dcc.Graph(id="graf3", figure=graf3)
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="graf5", figure=graf5)
        ]),
        dbc.Col([
            dcc.Graph(id="graf0", figure=graf0)
        ])
    ])
])

# Este row es una prueba
row = html.Div(
    [dbc.Row(dbc.Col(html.Div("Gráficos de análisis exploratorio")))
     ], style={})

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

slider = dcc.Slider(id="slider",
                    min=bd["year_factura"].min(),
                    max=bd["year_factura"].max(),
                    value=bd["year_factura"].max(),
                    marks={str(year): str(year) for year in bd["year_factura"].unique()}, step=None
                    )

#################################################################################################################################
############################################################## CONTENIDO #########################################################
content = html.Div([
    html.H1(["Offcorss Dash mock-up"], style=CONTENT_STYLE),
    row,
    dropdown1,
    slider,
    graphs
], style={"margin-left": "10rem"})

hoja_principal = html.Div([
    html.Div(dbc.Row(dbc.Col(sidebar(False))), style={"display": "none"}),
    
    dbc.Row(dbc.Col(main_page(app, True)))
])

app.layout = html.Div([
    hoja_principal,
    dcc.Location(id="url"),  # refresh = False
], id="page-content")

hoja_1_layout = html.Div([
    sidebar(True), content, main_page(app, False),
    html.Div(id='page-1-content')
])

hoja_2_layout = html.Div([
    html.Div(id='page-2-content'),
    html.H1("Hoja 2 prueba"),
    main_page(app, False),
    sidebar(True)
])


################################################################################################################################
####################################################### INTERACTIVIDAD #########################################################

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
    elif "link-hoja2" in changed_id or "button-cluster" in changed_id:
        return hoja_2_layout
    else:
        return hoja_principal

# @app.callback(Output("graf1", "figure"), Input("slider", "value"))
def change_graphs(year_value):

    df = bd_grupo1[bd_grupo1["year_factura"] == year_value]
    graf1_a = px.bar(df, x="mes_factura", y="vlr_neto_M", color="tipo_tienda", width=600, height=400,
                     color_discrete_map={
                         "TIENDA PROPIA": "gold",
                         "TIENDA VIRTUAL": "black",
                         "FRANQUICIAS": "silver"
                     },
                     category_orders={"tipo_tienda": [
                         "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
                     title="Ingresos por canal (Millones COP)")
    graf1_a.update_layout(xaxis_tickangle=90)
    return graf1_a


if __name__ == "__main__":
    app.run_server(debug=True)
