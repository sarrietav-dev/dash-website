import os
import dash
import random
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.Img(src=app.get_asset_url("ddg.png"))
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
    "background-color": "#FBD600"
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
                    map_graph
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
    ])
])

content = html.Div([
    html.Div(style=CONTENT_STYLE), graphs
], style={})

app.layout = html.Div([navbar, content])

if __name__ == "__main__":
    app.run_server(debug=True)
