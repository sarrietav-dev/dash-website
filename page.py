import os
import dash
import random
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

from graphs import *
from styles import *
from layouts import main_page, sidebar


app = dash.Dash(external_stylesheets=[
                dbc.themes.LUX], suppress_callback_exceptions=True)


# Aca van todas la gráficas:
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
            dbc.DropdownMenu(
                label="Options",
                id="date_dropdown",
                children=[
                    dbc.DropdownMenuItem("Year"),
                    dbc.DropdownMenuItem("Trim_año"),
                    dbc.DropdownMenuItem("Year_factura")
                ])
        ),
        dbc.Col([
            dbc.RadioItems(
                id="radio_items",
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
            dcc.Graph(id="graf5", figure=graf5)
        ]),
        dbc.Col([
            dcc.Graph(id="graph0", figure=graf0)
        ])
    ])
])

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

row = html.Div(
    [dbc.Row(dbc.Col(html.H5("Resumen de la base:")))
     ], style={})


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

#----------------------------------------------------------------- Content
content = html.Div([
    html.H1(["Offcorss Dash mock-up"], style=CONTENT_STYLE),
    row,
    summary,
    dropdown1,
    graphs,
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H5("Frecuencia tiendas físicas"),
                map_graph1
            ]),
            dbc.Col([
                html.H5("Frecuencia tiendas virtuales"),
                map_graph2
            ]),
        ])
    ]),
], style={"margin-left": "10rem"})

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
    html.Div(id='page-2-content'),
    html.H1("Hoja 2 prueba"),
    main_page(app, False),
    sidebar(True),
    html.H1(str(np.array(bd_unicos.iloc[:, 1])), style={
            "margin-left": "5rem"}),
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


# TODO: Make a callback for graph1 based on year, trim_año or year_factura for x. And some bullet points for vlr_neto and qt_facturas.
@app.callback(
    Output("graf1", "figure"),
    [Input("date_dropdown"), Input("radio_items")]
)
def foo(drop, radio):
    pass


# TODO: Make a callback that changes graph1 and graph3 based on vlr_neto and qt_facturas.
if __name__ == "__main__":
    app.run_server(debug=True)
