import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


######################################################################## CARGA DE BASES DE DATOS:
bd_agr_month = pd.read_csv("data/offcorss_agr_tienda_año_mes.csv",
                 sep=";")

bd_agr_year = pd.read_csv("data/offcorss_agregada_año.csv",
                 sep=";")

#########################################################################TRANSFORMACION DE BASES DE DATOS

bd_agr_month["ticket_prom"] = bd_agr_month["vlr_neto"] / bd_agr_month["qt_facturas_unq"]
bd_agr_month["year"] = bd_agr_month["year_factura"].str[:4]
bd_agr_month["trim_año"] = bd_agr_month["year"].astype(str) + "-Q" + bd_agr_month["trimestre"].astype(str)

# GRAFICA 1: BAR Ingresos por canal
graf1 = px.bar(bd_agr_month, x="year_factura", y="vlr_neto", color="tipo_tienda", width=600, height=400,

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
               color="tipo_tienda", width=800, height=400,
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

# GRAFICA 5: LINE Evolución ticket promed
graf5 = px.line(bd_agr_month, x="year_factura", y="ticket_prom",
                color="tipo_tienda", width=800, height=400,
                color_discrete_map={
                    "TIENDA PROPIA": "gold",
                    "TIENDA VIRTUAL": "black",
                    "FRANQUICIAS": "silver"
                },
                category_orders={"tipo_tienda": [
                    "TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]},
                title="Evolución ticket promedio")

graf5.update_layout(xaxis_tickangle=90)
