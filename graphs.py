import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_table

# CARGA DE BASES DE DATOS:
bd_agr_month = pd.read_csv("data/offcorss_agr_tienda_año_mes.csv",
                           sep=";")

bd_agr_year = pd.read_csv("data/offcorss_agregada_año.csv",
                          sep=";")

bd_unicos = pd.read_csv("data/offcorss_totales_unicos.csv",
                 sep=";")

#########################################################################TRANSFORMACION DE BASES DE DATOS

bd_agr_month["ticket_prom"] = bd_agr_month["vlr_neto"] / \
    bd_agr_month["qt_facturas_unq"]
bd_agr_month["year"] = bd_agr_month["year_factura"].str[:4]
bd_agr_month["trim_año"] = bd_agr_month["year"].astype(
    str) + "-Q" + bd_agr_month["trimestre"].astype(str)


# % Crecimiento MoM por canal

var = "vlr_neto" # o vlr_neto

para = ["TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]
for t in para:
    deltas = []
    temp = bd_agr_month[bd_agr_month["tipo_tienda"] == t][var].reset_index() 
    for i, e in enumerate(temp[var]):
        meses_ex = [0,1,2,3,4,5,6,7,8,9,10,11]
        if i in meses_ex:
            a = None
        else:
            a = float((e/temp[var][i-12])-1)
        deltas.append(a)
    deltas = pd.Series(deltas)
    if t == "TIENDA PROPIA":        
        deltas_todo =   deltas
    else:
        deltas_todo =  pd.concat([deltas_todo, deltas], axis = 1)
deltas_todo = pd.concat([pd.Series(bd_agr_month["year_factura"].unique()), deltas_todo], axis = 1)
deltas_todo = deltas_todo.iloc[12:,]
deltas_todo.columns = ["fecha", "TP", "TV", "FR"]


# GRAFICA 0: variaciones MoM
graf0 = go.Figure(layout =
go.Layout(
    autosize=False,
    width=600,
    height=400,
title='Variaciones MoM por canal'
    )
                  )

graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["TP"],
                    mode='lines+markers',
                    name='TP'))
graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["TV"],
                    mode='lines+markers',
                    name='TV'))
graf0.add_trace(go.Scatter(x=deltas_todo["fecha"], y=deltas_todo["FR"],
                    mode='lines+markers',
                    name='FR'))




# GRAFICA 1: BAR Ingresos por canal
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

# GRAFICA 2: BAR Número de ventas por canal
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


# GRAFICA 3: PIE Share de ingresos
graf3 = px.pie(bd_agr_month, values='vlr_neto', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Ingresos por canal')

# GRAFICA 4:PIE Share de número de ventas
graf4 = px.pie(bd_agr_month, values='qt_facturas_unq', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Número de ventas por canal')

# GRAFICA 5: LINE Evolución ticket promedio
graf5 = px.line(bd_agr_month, x="year_factura", y="ticket_prom",
                color="tipo_tienda", width=600, height=400,
                color_discrete_map={
                    "TIENDA PROPIA": "gold",
                    "TIENDA VIRTUAL": "black",
                    "FRANQUICIAS": "silver"
                },
                category_orders={"tipo_tienda": [
                    "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
                title="Evolución ticket promedio")
graf5.update_layout(xaxis_tickangle=90)
