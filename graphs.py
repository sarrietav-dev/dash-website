import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_table
import os
import random
import dash_core_components as dcc

# CARGA DE BASES DE DATOS:
bd_agr_month = pd.read_csv("data/offcorss_agr_tienda_año_mes.csv",
                           sep=";")

bd_agr_year = pd.read_csv("data/offcorss_agregada_año.csv",
                          sep=";")

bd_unicos = pd.read_csv("data/offcorss_totales_unicos.csv",
                        sep=";")


bd_frec = pd.read_csv("data/offcorss_frecuencia_acum.csv",
                      sep=";")

bd_frec_canal = pd.read_csv("data/frecuencia_acumulada_canal.csv",
                      sep=";")



# TRANSFORMACION DE BASES DE DATOS

bd_agr_month["ticket_prom"] = bd_agr_month["vlr_neto"] / \
    bd_agr_month["qt_facturas_unq"]
bd_agr_month["year"] = bd_agr_month["year_factura"].str[:4]
bd_agr_month["trim_año"] = bd_agr_month["year"].astype(
    str) + "-Q" + bd_agr_month["trimestre"].astype(str)

# Para grafica 5_1
bd_agr_month2 = bd_agr_month[["trim_año", "tipo_tienda", "vlr_neto", "qt_facturas_unq"]]\
                        .groupby(["trim_año", "tipo_tienda"]).sum().reset_index()
bd_agr_month2["ticket_prom"] = bd_agr_month2["vlr_neto"] / bd_agr_month2["qt_facturas_unq"]

# Para gráfica 5_2
bd_agr_month3 = bd_agr_month[["year", "tipo_tienda", "vlr_neto", "qt_facturas_unq"]]\
                        .groupby(["year", "tipo_tienda"]).sum().reset_index()
bd_agr_month3["ticket_prom"] = bd_agr_month3["vlr_neto"] / bd_agr_month3["qt_facturas_unq"]

# -------------------------------------------------------------- TRANSFORMACION PARA TABLE1
bd_unicos["year_factura"] = "TOTAL"
cols = ['year_factura', 'registros', 'fact_uniq',
        'cli_uniq', 'freq', 'revenue', 'desde',  'hasta']
bd_unicos2 = bd_unicos[cols]
bd_unicos2 = bd_unicos2.iloc[:, :6]
bd_unicos_merged = pd.concat([bd_agr_year.iloc[:, :-2], bd_unicos2])
bd_unicos_merged = bd_unicos_merged.reset_index(drop=True)

bd_unicos_merged.columns = [
    'Año', 'Registros(Núm.)', 'Compras(Núm.)', 'Clientes únicos(Núm.)', 'Frecuencia', 'Revenue(M_COP)']
bd_unicos_merged["Revenue(M_COP)"] = (
    bd_unicos_merged["Revenue(M_COP)"]/1000000).apply('{:,.0f}'.format)
bd_unicos_merged["Frecuencia"] = (
    bd_unicos_merged["Frecuencia"]).apply('{:,.2f}'.format)
bd_unicos_merged["Registros(Núm.)"] = (
    bd_unicos_merged["Registros(Núm.)"]).apply('{:,.0f}'.format)
bd_unicos_merged["Compras(Núm.)"] = (
    bd_unicos_merged["Compras(Núm.)"]).apply('{:,.0f}'.format)
bd_unicos_merged["Clientes únicos(Núm.)"] = (
    bd_unicos_merged["Clientes únicos(Núm.)"]).apply('{:,.0f}'.format)


# -------------------------------------------------------------- % Crecimiento MoM por canal

var = "vlr_neto"  # o vlr_neto

para = ["TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]
for t in para:
    deltas = []
    temp = bd_agr_month[bd_agr_month["tipo_tienda"] == t][var].reset_index()
    for i, e in enumerate(temp[var]):
        meses_ex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        if i in meses_ex:
            a = None
        else:
            a = float((e/temp[var][i-12])-1)
        deltas.append(a)
    deltas = pd.Series(deltas)
    if t == "TIENDA PROPIA":
        deltas_todo = deltas
    else:
        deltas_todo = pd.concat([deltas_todo, deltas], axis=1)
deltas_todo = pd.concat(
    [pd.Series(bd_agr_month["year_factura"].unique()), deltas_todo], axis=1)
deltas_todo = deltas_todo.iloc[12:, ]
deltas_todo.columns = ["fecha", "TP", "TV", "FR"]


#--------------------------------------------------------------------------------------- GRAFICA 0: variaciones MoM por canal

layout = go.Layout(
    autosize=False,
    width=600,
    height=400,
    title='Variaciones MoM por canal',
    title_x=0.5,
    title_y=0.8,
    yaxis_title="%variación",
    xaxis_title="mes",
    xaxis=dict(
        showline=False,
        showgrid=False
    ),
    yaxis=dict(
        showline=True,
        showgrid=False
    ),
    plot_bgcolor="whitesmoke"
)
graf0 = go.Figure(layout=layout)
graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["TP"],
                           mode='lines+markers',
                           name='TP',
                           line=dict(color="gold")
                           ))

graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["TV"],
                           mode='lines+markers',
                           name='TV',
                           line=dict(color="black")
                           ))
graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["FR"],
                           mode='lines+markers',
                           name='FR',
                           line=dict(color="grey")

                           ))


#------------------------------------------------------------------------------------- GRAFICA 1: BAR Ingresos por canal

graf1 = px.bar(bd_agr_month, x="year_factura", y="vlr_neto", color="tipo_tienda", width=800, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               category_orders={"tipo_tienda": [
                   "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
               title="Ingresos por canal (Millones COP)")
graf1.update_layout(xaxis_tickangle=90)

#-------------------------------------------------------------------------------- GRAFICA 2: BAR Número de ventas por canal

graf2 = px.bar(bd_agr_month, x="year_factura", y="qt_facturas_unq",
               color="tipo_tienda", width=600, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               category_orders={"tipo_tienda": [
                   "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
               title="Número de ventas por canal")
graf2.update_layout(xaxis_tickangle=90)


#-------------------------------------------------------------------------------------GRAFICA 3: PIE Share de ingresos

graf3 = px.pie(bd_agr_month, values='vlr_neto', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Ingresos por canal')

#-----------------------------------------------------------------------------------GRAFICA 4:PIE Share de número de ventas

graf4 = px.pie(bd_agr_month, values='qt_facturas_unq', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Número de ventas por canal')

#---------------------------------------------------------------------------------GRAFICA 5: LINE Evolución ticket promedio

graf5 = px.line(bd_agr_month, x="year_factura", y="ticket_prom",
                color="tipo_tienda", width=700, height=400,
                color_discrete_map={
                    "TIENDA PROPIA": "gold",
                    "TIENDA VIRTUAL": "black",
                    "FRANQUICIAS": "silver"
                },
                category_orders={"tipo_tienda": [
                    "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
                title="Evolución ticket promedio",
                )
graf5.update_layout(xaxis_tickangle=90)

#------------------------------------------------------GRAFICA 5.1: LINE Evolución ticket promedio por trimestre

graf5_1 = px.line(bd_agr_month2, x = "trim_año", y = "ticket_prom", 
            color = "tipo_tienda", width=600, height=400,
             color_discrete_map={
                "TIENDA PROPIA": "gold",
                "TIENDA VIRTUAL": "black",
                "FRANQUICIAS": "silver"
             },
             category_orders={"tipo_tienda": ["TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},             
            title = "Evolución ticket promedio",
            template = "simple_white")
graf5_1.update_layout(xaxis_tickangle=90)

#------------------------------------------------------GRAFICA 5.1: LINE Evolución ticket promedio por año

graf5_2 = px.line(bd_agr_month3, x = "year", y = "ticket_prom", 
            color = "tipo_tienda", width=600, height=400,
             color_discrete_map={
                "TIENDA PROPIA": "gold",
                "TIENDA VIRTUAL": "black",
                "FRANQUICIAS": "silver"
             },
             category_orders={"tipo_tienda": ["TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},             
            title = "Evolución ticket promedio",
            template = "simple_white")
graf5_2.update_layout(xaxis_tickangle=90)


#--------------------------------------------------------------------------- GRAFICA 6: LINEPLOT Frecuencia acumulada por año
año1 = bd_frec["yeard"].unique()[0]
año2 = bd_frec["yeard"].unique()[1]
año3 = bd_frec["yeard"].unique()[2]

layout = go.Layout(
    autosize=False,
    width=600,
    height=400,
    title='Frecuencia acumulada por mes',
    title_x=0.5,
    title_y=0.8,
    xaxis_title="mes",
    yaxis_title="frecuencia acumulada",
    xaxis=dict(
        showline=True,
        showgrid=True
    ),
    yaxis=dict(
        showline=True,
        showgrid=False
    ),
    plot_bgcolor="whitesmoke"
)

graf6 = go.Figure(layout=layout)
graf6.add_trace(go.Scatter(x=bd_frec[bd_frec["yeard"] == año1]["mes"], y=bd_frec[bd_frec["yeard"] == año1]["frec_acum"],
                           mode='lines+markers',
                           name=str(año1),
                           line=dict(color="black")
                           ))
graf6.add_trace(go.Scatter(x=bd_frec[bd_frec["yeard"] == año2]["mes"], y=bd_frec[bd_frec["yeard"] == año2]["frec_acum"],
                           mode='lines+markers',
                           name=str(año2),
                           line=dict(color="yellow")
                           ))
graf6.add_trace(go.Scatter(x=bd_frec[bd_frec["yeard"] == año3]["mes"], y=bd_frec[bd_frec["yeard"] == año3]["frec_acum"],
                           mode='lines+markers',
                           name=str(año3),
                           line=dict(color="tomato")
                           ))

#-------------------------------------------------------------------- GRAFICA 7: LINEPLOT Frecuencia acumulada por año por CANAL
año1 = bd_frec_canal["yeard"].unique()[0]
año2 = bd_frec_canal["yeard"].unique()[1]
año3 = bd_frec_canal["yeard"].unique()[2]

tv = bd_frec_canal["tipo_tienda"].unique()[0]
tp = bd_frec_canal["tipo_tienda"].unique()[1]
fr = bd_frec_canal["tipo_tienda"].unique()[2]

layout = go.Layout(
    autosize=False,
    width=650,
    height=400,
    title='Frecuencia acumulada por mes - CANAL',
    title_x=0.5,
    title_y=0.8,
    xaxis_title = "mes",
    yaxis_title = "frecuencia acumulada",
    xaxis=dict(
        showline=True,
        showgrid=True
            ),
    yaxis=dict(
        showline=True,
        showgrid=False
    ),
    plot_bgcolor="whitesmoke"
)

#________________________________________________________________Año 1
graf7 = go.Figure(layout = layout)
graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año1)&(bd_frec_canal["tipo_tienda"] == tp)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año1)&(bd_frec_canal["tipo_tienda"] == tp)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año1) + " " +str(tp),
                    line = dict(color = "black")
                          ))

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año1)&(bd_frec_canal["tipo_tienda"] == tv)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año1)&(bd_frec_canal["tipo_tienda"] == tv)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año1) + " " +str(tv),
                    line = dict(color = "grey")
                          ))

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año1)&(bd_frec_canal["tipo_tienda"] == fr)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año1)&(bd_frec_canal["tipo_tienda"] == fr)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año1) + " " +str(fr),
                    line = dict(color = "silver")
                          ))
#__________________________________________________________________Año 2

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año2)&(bd_frec_canal["tipo_tienda"] == tp)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año2)&(bd_frec_canal["tipo_tienda"] == tp)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año2) + " " +str(tp),
                    line = dict(color = "orange")
                          ))

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año2)&(bd_frec_canal["tipo_tienda"] == tv)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año2)&(bd_frec_canal["tipo_tienda"] == tv)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año2) + " " +str(tv),
                    line = dict(color = "gold")
                          ))

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año2)&(bd_frec_canal["tipo_tienda"] == fr)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año2)&(bd_frec_canal["tipo_tienda"] == fr)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año2) + " " +str(fr),
                    line = dict(color = "yellow")
                          ))
#________________________________________________________________ Año 3

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año3)&(bd_frec_canal["tipo_tienda"] == tp)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año3)&(bd_frec_canal["tipo_tienda"] == tp)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año3) + " " +str(tp),
                    line = dict(color = "red")
                          ))

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año3)&(bd_frec_canal["tipo_tienda"] == tv)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año3)&(bd_frec_canal["tipo_tienda"] == tv)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año3) + " " +str(tv),
                    line = dict(color = "tomato")
                          ))

graf7.add_trace(go.Scatter(x= bd_frec_canal[(bd_frec_canal["yeard"] == año3)&(bd_frec_canal["tipo_tienda"] == fr)]["mes"], 
                           y= bd_frec_canal[(bd_frec_canal["yeard"] == año3)&(bd_frec_canal["tipo_tienda"] == fr)]["frec_acum"],                           
                    mode='lines+markers',
                    name=str(año3) + " " +str(fr),
                    line = dict(color = "pink")
                          ))


#------------------------------------------------------------------------------------------------------------------ MAPAS
# Data real del mapa:
centro_region_agr_2019 = pd.read_csv(
    "data/centro_region_agr_2019.csv", sep=";", encoding="Latin-1")
# ------------------ info geo de: http://blog.jorgeivanmeza.com/wp-content/uploads/2008/09/municipioscolombiacsv.txt

# ----Info geográfica de las tiendas físicas:
#centro_region_agr_2019_TP = centro_region_agr_2019[centro_region_agr_2019["tipo_tienda"] != "TIENDA VIRTUAL"]
centro_region_agr_2019_TP = centro_region_agr_2019[(centro_region_agr_2019["tipo_tienda"] != "TIENDA VIRTUAL")
                                                   & (centro_region_agr_2019["latitud_c"] > 0)
                                                   & (centro_region_agr_2019["frecuencia"] < 4)]  # excluir San Andrés??

# ----Info geográfica de las tiendas virtuales:
centro_region_agr_2019_TV = centro_region_agr_2019[(centro_region_agr_2019["tipo_tienda"] == "TIENDA VIRTUAL")
                                                   & (centro_region_agr_2019["latitud_m"] > 0)
                                                   & (centro_region_agr_2019["frecuencia"] < 4)]


map1 = px.scatter_mapbox(centro_region_agr_2019_TP, lat="latitud_c", lon="longitud_c", color="frecuencia",
                         size="visitas", mapbox_style="carto-positron",
                         height=700, width=600, zoom=4.5)

map2 = px.scatter_mapbox(centro_region_agr_2019_TV, lat="latitud_m", lon="longitud_m", color="frecuencia",
                         size="visitas", mapbox_style="carto-positron",
                         height=700, width=600, zoom=4.5)


map_graph1 = dcc.Graph(
    id="map_graph1",
    figure=map1
)

map_graph2 = dcc.Graph(
    id="map_graph2",
    figure=map2
)

tabla1 = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in bd_unicos_merged.columns],
    data=bd_unicos_merged.to_dict('records')
)
