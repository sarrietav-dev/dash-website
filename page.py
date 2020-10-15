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

#################################################################################################################################
################################################## CARGA DE DATA ORIGINAL #######################################################

#####################################################################################################################################
############################################### Components #######################################################################

app = dash.Dash(external_stylesheets=[
                dbc.themes.LUX], suppress_callback_exceptions=True)

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

#################################################################################################################################
############################################################## CONTENIDO #########################################################
content = html.Div([
    html.H1(["Offcorss Dash mock-up"], style=CONTENT_STYLE),
    row,
    dropdown1,
    graphs
], style={"margin-left": "10rem"})


app.layout = html.Div([
    dcc.Location(id="url"),  # refresh = False
    sidebar,
    html.Div(id="page-content")
])

hoja_1_layout = html.Div([
    sidebar, content,
    html.Div(id='page-1-content')
])

hoja_2_layout = html.Div([
    html.Div(id='page-2-content'),
    html.H1("Hoja 2 prueba"),
    sidebar
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
    Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/hoja-1":
        return hoja_1_layout
    elif pathname == "/hoja-2":
        return hoja_2_layout


if __name__ == "__main__":
    app.run_server(debug=True)
