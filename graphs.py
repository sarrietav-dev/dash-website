import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

bd = pd.read_csv("data/offcorss_transac_agr_202010102240.csv",
                 sep=";")

# AGRUPACION 1

bd_grupo1 = bd[["year_mes_factura", "trimestre", "year_factura", "tipo_tienda",  "vlr_neto", "qt_facturas_unq", "qt_articulo_unq"]].\
    groupby(["year_mes_factura", "trimestre",
             "year_factura", "tipo_tienda"]).sum()

bd_grupo1 = bd_grupo1.reset_index()
bd_grupo1["vlr_neto_M"] = bd_grupo1["vlr_neto"] / \
    1000000  # Manejar la cifra en millones?
bd_grupo1["ticket_prom"] = bd_grupo1["vlr_neto"] / bd_grupo1["qt_facturas_unq"]

# PROCEDIMIENTO 1 +  GRAFICA 0
# % Crecimiento MoM

para = ["TIENDA PROPIA", "TIENDA VIRTUAL", "FRANQUICIAS"]
for t in para:
    deltas = []
    temp = bd_grupo1[bd_grupo1["tipo_tienda"] == t]["vlr_neto"].reset_index()
    for i, e in enumerate(temp["vlr_neto"]):
        meses_ex = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        if i in meses_ex:
            a = None
        else:
            a = float((e/temp["vlr_neto"][i-12])-1)
        deltas.append(a)
    deltas = pd.Series(deltas)
    if t == "TIENDA PROPIA":
        deltas_todo = deltas
    else:
        deltas_todo = pd.concat([deltas_todo, deltas], axis=1)
deltas_todo = pd.concat(
    [pd.Series(bd_grupo1["year_mes_factura"].unique()), deltas_todo], axis=1)
deltas_todo = deltas_todo.iloc[12:, ]
deltas_todo.columns = ["fecha", "TP", "TV", "FR"]

# GRAFICA 0: Ingresos month over mont MoM

graf0 = go.Figure(layout=go.Layout(
    autosize=False,
    width=800,
    height=400,
    title='Variaciones MoM por canal')

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
graf1 = px.bar(bd_grupo1, x="year_mes_factura", y="vlr_neto_M", color="tipo_tienda", width=600, height=400,
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
graf2 = px.bar(bd_grupo1, x="year_mes_factura", y="qt_facturas_unq",
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
graf3 = px.pie(bd_grupo1, values='vlr_neto_M', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Ingresos por canal')

# GRAFICA 4:PIE Share de número de ventas
graf4 = px.pie(bd_grupo1, values='qt_facturas_unq', names='tipo_tienda', color="tipo_tienda",  width=400, height=400,
               color_discrete_map={
                   "TIENDA PROPIA": "gold",
                   "TIENDA VIRTUAL": "black",
                   "FRANQUICIAS": "silver"
               },
               title='%Número de ventas por canal')

# GRAFICA 5: LINE Evolución ticket promedio
graf5 = px.line(bd_grupo1, x="year_mes_factura", y="ticket_prom",
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