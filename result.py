import pandas as pd
import os 
from sqlalchemy import create_engine
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

engine = create_engine('postgresql://postgres:Team842020*@offcorssdb.cfinmnv8hcp0.us-east-2.rds.amazonaws.com/postgres')


#f_beb = pd.read_sql_query('select * from "vw_top10_fem_beb"',con=engine)

f_beb = pd.read_csv("data/vw_top10_fem_beb_202011101811.csv",sep = ";")
f_beb["porc_cantidad"] = 0.10

content3 = html.Div([

html.Div([
        dbc.Button("Primi", size="lg", className="mb-2", color="warning",  id="primi_niño"),
        dbc.Button("Bebe-Niño", size="lg", className="mb-2", color="warning", id="bebe_niño"),
        
]),

html.Div([
        dbc.Button("Primi", size="lg", className="mb-2", color="warning",  id="primi_niño"),
        dbc.Button("Bebe-Niño", size="lg", className="mb-2", color="warning", id="bebe_niño"),
    
]),


html.Div([
    dbc.Row(
        ),
    dbc.Row(
        )
]),

], style = {"margin-left":"20rem"})



#_______________________________________________ GRAFICOS Y TABLAS _____________________________________________________

px.bar(f_beb[f_beb["clu"] == 0][["grupo_articulo", "cantidad", "porc_cantidad"]].reset_index(drop=True).sort_values(by="cantidad")
       , x= "cantidad", y = "grupo_articulo",
       title = "TOP 10 productos clúster " + str(0),
       hover_data = ["porc_cantidad"],
       color_discrete_map={
                "": "gold"
             }      
      )





