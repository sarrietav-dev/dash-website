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
cluster_names_p3 = {0:"low_price ", 1:"medium_price", 2:"high_price", 3:"Fans"}
f_beb["clu_name"] = f_beb["clu"].map(cluster_names_p3) 

#_______________________________________________ GRAFICOS Y OBJETOS _____________________________________________________

rg1 = px.bar(f_beb[f_beb["clu"] == 0][["grupo_articulo", "cantidad", "porc_cantidad"]].reset_index(drop=True).sort_values(by="cantidad")
       , x= "cantidad", y = "grupo_articulo",
       title = "TOP 10 productos clúster " + str(0),
       hover_data = ["porc_cantidad"],
       width = 600,
       color_discrete_map={
                "": "gold"
             }      
)


rg2 = px.bar(f_beb[f_beb["clu"] == 0][["grupo_articulo", "cantidad", "porc_cantidad"]].reset_index(drop=True).sort_values(by="cantidad")
       , x= "cantidad", y = "grupo_articulo",
       title = "TOP 10 productos clúster " + str(0),
       hover_data = ["porc_cantidad"],
       width = 600,
       color_discrete_map={
                "": "grey"
             }      
)




dropdown_clu = dcc.Dropdown( 
    placeholder="Options",
    id="dropdown_clu_p3",
    value=[],
    className="dropdown m-3",
    options= [{"label":e, "value":e} for e in f_beb["clu_name"].unique()],    
    searchable = False
    
)

dropdown_prod = dcc.Dropdown( 
    placeholder="Options",
    id="dropdown_prdo_p3",
    value=[],
    className="dropdown m-3",
    options = [{"label":e, "value":e} for e in f_beb["grupo_articulo"].sort_values().unique()],
    searchable = False
    
)







