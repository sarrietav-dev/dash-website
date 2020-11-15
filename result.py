import pandas as pd
import os 
from sqlalchemy import create_engine
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go

engine = create_engine('postgresql://postgres:Team842020*@offcorssdb.cfinmnv8hcp0.us-east-2.rds.amazonaws.com/postgres')

df_res = pd.read_sql_query('select * from "vw_offcorss_descar_clu_agr"',con=engine)
cluster_names_p3 = {0:"sale_hunters", 1:"average_customer", 2:"selective_customer", 3:"offcorss_fans"}
df_res["clu_name"] = df_res["clu"].map(cluster_names_p3)
df_res2 = df_res[df_res["clu"].isna() == False] # Remove NAS
df_res2 = df_res2[df_res2["grupo_articulo"].isnull() == False] # Remove None

# Agrupación 1
df_grupo_art = df_res2.groupby(["genero","edad", "grupo_articulo", "clu_name"]).sum().reset_index()

gen = "MASCULINO"
ed = "PRIMI"
clu = "sale_hunters"
ga = "CAMISA"

tabla_grupo_art = df_grupo_art[(df_grupo_art["genero"] == gen) &\
                               (df_grupo_art["edad"] == ed) &\
                               (df_grupo_art["clu_name"] == clu)]\
                                [["grupo_articulo", "cantidad", "freq_relativa"]]\
                                .reset_index(drop=True).sort_values(by="cantidad", ascending = False)

# Agrupación 2
df_tipo_art = df_res2.groupby(["genero","edad", "grupo_articulo","tipo_articulo" , "tipo_tejido", "clu_name"]).sum().reset_index()

tabla_tipo_art = df_tipo_art[(df_tipo_art["genero"] == gen) &\
                               (df_tipo_art["edad"] == ed) &\
                               (df_tipo_art["clu_name"] == clu)&\
                               (df_tipo_art["grupo_articulo"] == ga)]\
                                [["tipo_articulo", "cantidad", "freq_relativa", "tipo_tejido"]]\
                                .reset_index(drop=True).sort_values(by="cantidad", ascending = False)


#_______________________________________________ GRAFICOS Y OBJETOS ______________________________________________________________

rg1 = px.bar(tabla_grupo_art.head(10).sort_values(by="cantidad"), x= "cantidad", y = "grupo_articulo",
       title = "TOP 10 productos clúster " + clu +" "+ gen + " " + ed,
       hover_data = ["freq_relativa"],
       color_discrete_map={
                "": "gold"
             }      
)

rg2 = go.Figure(go.Bar(x=tabla_tipo_art[tabla_tipo_art["tipo_tejido"] == 'TEJIDO PLANO']["cantidad"], 
                       y=tabla_tipo_art[tabla_tipo_art["tipo_tejido"] == 'TEJIDO PLANO']["tipo_articulo"], 
                       name='TEJIDO PLANO',
                      orientation='h',
                      marker_color='silver'))

rg2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
rg2.update_layout(title_text='Top 10 tipos de ' +  ga)


dropdown_clu = dcc.Dropdown( 
    placeholder="Options",
    id="dropdown_clu_p3",
    value=[],
    className="dropdown m-3",
    options= [{"label":e, "value":e} for e in df_res2["clu_name"].unique()],    
    searchable = False,
    style={'height': '30px', 'width': '300px'}
    
)

dropdown_prod = dcc.Dropdown( 
    placeholder="Options",
    id="dropdown_grupo_p3",
    value=[],
    className="dropdown m-3",
    options = [{"label":e, "value":e} for e in df_res2["grupo_articulo"].sort_values().unique()],
    searchable = False,
    style={'height': '30px', 'width': '300px'}
    
)

dropdown_top = dcc.Dropdown( 
    placeholder="Options",
    id="dropdown_top10_p3",
    value=[],
    className="dropdown m-3",
    options = [{"label":"Top 10", "value": "head"}, {"label":"Bottom 5", "value":"tail"}],
    searchable = False,
    style={'height': '30px', 'width': '150px'}
    
)







