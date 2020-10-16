import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def main_page(app):
    main_page = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(
                    html.Img(src=app.get_asset_url("banner.webp")),
                    style={
                        "position": "absolute",
                        "background-color": "#0F0",
                        "display": "inline-block"
                    })
            ])
        ]),
    ])
    return main_page
