# Importing all the required packages
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle
from sqlalchemy import create_engine

# -----------------------------------------------------------------------------------Function Normalize
# Input = df, DataFrame we are interested in normalizing
# This is the Min/Max scaling method


def normalize(df):
    result = df.copy()

    for feature_name in df.columns:
        max_val = df[feature_name].max()
        min_val = df[feature_name].min()
        result[feature_name] = (
            df[feature_name] - min_val) / (max_val - min_val)

    return result


# --------------------------------------------------------------------------------------- Importar df clasificado
engine = create_engine(
    'postgresql://postgres:Team842020*@offcorssdb.cfinmnv8hcp0.us-east-2.rds.amazonaws.com/postgres')

df_clasif = pd.read_sql_query(
    'select * from "vw_offcorss_customer" limit 25000', con=engine)

# --------------------------------------------------------------------------------------- Importar df
#df = pd.read_csv('data/offcorss_customer_202011011419_2.csv', sep=";")

df = df_clasif.copy()  # Aca cuando se selecciona la base completa de los 1.3M de clientes

# Creación de dos variables adicionales:
df["ran_meses"] = df["max_meses"]-df["min_meses"]
df["compras_x_visita"] = df["compras"] / df["visitas"]

# ____________________________________________________________________________________________APLICACIÓN AUTOMÁTICA CLASIFICACIÓN
##para_pca = ["revenue", "visitas","compras"]
##
##scaler = StandardScaler()
##df_seg = scaler.fit_transform(df[para_pca])
##pca = PCA()
# pca.fit(df_seg)
##pca = PCA(n_components = 1)
##pca_df = pca.fit_transform(df_seg)
##pca_df = pd.DataFrame(data = pca_df, columns = ["Dim1"])
##scores_pca = normalize(pca_df)
##
# Separación del percentil 0.95 de la base para creación de clúster con mayores a dicho percentil:
##df["score_pca"] = scores_pca
##q95 = df["score_pca"].quantile(0.95)
##df_may95 = df[df["score_pca"]> q95]
##df_men95 = df[df["score_pca"]<= q95]
##
# df_men95_norm = normalize(df_men95[["recencia", "revenue", "visitas","compras","precio_promedio_log",
##                        "ticket_prom_compra", "ticket_prom_compra_log",  "ran_meses", "avg_meses_log",
# "avg_meses", "precio_promedio","compras_x_visita", "compras_x_visita_log"]])
##
##
# ----------------------------------------------------------- Aplicación del algoritmo:
##
##df2= df_men95_norm[["avg_meses", "precio_promedio"]]
##
##kmeans = pickle.load(open("models/model.pkl", "rb"))
# kmeans.fit(df2)
##labels = kmeans.predict(df2)
##centroids = kmeans.cluster_centers_
# kmeans.inertia_
##
# --------------------------------------------------------------- Centroides:
##centroids = kmeans.cluster_centers_
##df_centroides = pd.DataFrame(centroids)
##df_centroides.columns = list(df2.columns)
##df_centroides = df_centroides.transpose()
##
# --------------------------------------------------------------- Union de las bases y pegar clasificación de clústeres:
##df_men95["cluster"] = labels
##df_may95["cluster"] = "f"
##df_cluster = df_men95.append(df_may95)

# ____________________________________________________________________________________________APLICACIÓN MANUAL CLASIFICACIÓN
##scaler = StandardScaler()
##df_seg = scaler.fit_transform(df[["revenue", "visitas","compras"]])
##pca = PCA()
# pca.fit(df_seg)
##pca = PCA(n_components = 1)
##pca_df = pca.fit_transform(df_seg)
##pca_df = pd.DataFrame(data = pca_df, columns = ["Dim1"])
##scores_pca = normalize(pca_df)

##df["score_pca"] = scores_pca
##q95 = df["score_pca"].quantile(0.95)
##
##bins = [0, 36466, 60479,df["precio_promedio"].max()]
##labels = ["<36k", "36k-60k", ">60k"]

##df["rango_precio"] = pd.cut(df["precio_promedio"], bins=bins, labels=labels)
##df["cluster"] = [0  if x =="<36k" else 1 if x == "36k-60k" else 2  for x in df["rango_precio"]]
##df["cluster"] =  list(np.select([df["score_pca"]>q95, df["score_pca"]<=q95], [9, df["cluster"]]))

df_cluster = df.copy()
cluster_names = {0: "sale_hunters", 1: "average_customer",
                 2: "selective_customer", 3: "offcorss_fans"}
df_cluster["cluster_name"] = df_cluster["clu"].map(cluster_names)


# _______________________________________________GRAFICOS DE MODELO _______________________________________________________________

# Modificaciones a df3 para graficar
df_cluster2 = df_cluster.copy()
df_cluster2["constante_cli"] = 1
df_cluster2["constante_size"] = 1
df_cluster2["recencia_meses"] = df_cluster2["recencia"] / 30

# -------------------------------------------------------------------Heatmap de centroides (MG2)

heat = df_cluster[["visitas", "compras", "revenue", "recencia", "ticket_prom_compra", "avg_meses",
                   "precio_promedio", "compras_x_visita", "cluster_name"]]
heat1 = heat.groupby("cluster_name").mean().reset_index()

# Para el resumen de tablas de clúster
heat2 = heat.groupby("cluster_name").mean().reset_index()
heat2 = heat2.set_index("cluster_name")  # Para el resumen de tablas de clúster

mg2 = px.imshow(normalize(heat1.iloc[:, 1:]),
                labels=dict(y="cluster"),
                title="Promedios normalizados por principales variables",
                y=list(heat1["cluster_name"]),
                width=700, height=600,
                color_continuous_scale='Cividis_r'
                )
# --------------------------------------------------------------------------------# Para tabla resúmen
tablaA = pd.concat([df_cluster["cluster_name"].value_counts(), heat2], axis=1)
tablaA = tablaA.rename(columns={"cluster_name": "clientes"})
tablaA = pd.DataFrame(tablaA.loc["sale_hunters"]).transpose()
tablaA = pd.DataFrame(tablaA.iloc[0, 0:].apply("{:.2f}".format)).transpose()

tablaB = pd.concat([df_cluster["cluster_name"].value_counts(), heat2], axis=1)
tablaB = tablaB.rename(columns={"cluster_name": "clientes"})
tablaB = pd.DataFrame(tablaB.loc["average_customer"]).transpose()
tablaB = pd.DataFrame(tablaB.iloc[0, 0:].apply("{:.2f}".format)).transpose()

tablaC = pd.concat([df_cluster["cluster_name"].value_counts(), heat2], axis=1)
tablaC = tablaC.rename(columns={"cluster_name": "clientes"})
tablaC = pd.DataFrame(tablaC.loc["selective_customer"]).transpose()
tablaC = pd.DataFrame(tablaC.iloc[0, 0:].apply("{:.2f}".format)).transpose()

tablaD = pd.concat([df_cluster["cluster_name"].value_counts(), heat2], axis=1)
tablaD = tablaD.rename(columns={"cluster_name": "clientes"})
tablaD = pd.DataFrame(tablaD.loc["offcorss_fans"]).transpose()
tablaD = pd.DataFrame(tablaD.iloc[0, 0:].apply("{:.2f}".format)).transpose()

# -------------------------------------------------------------------Scatter pares de variables (MG3)

mg3 = px.scatter(df_cluster2, x="recencia_meses",
                 y="avg_meses",
                 color="cluster_name",
                 title='Scatter pares de variables',
                 height=550)

#---------------------------------------------------------------------Treemap (MG4)

# Treemap clientes por canal/region/ciudad/cluster
mg4 = px.treemap(df_cluster2, path=[px.Constant('CLIENTES:  ' + str(df_cluster2["constante_cli"].sum())),
                                    "canal_det", 'region',  "cluster_name"],
                 values='constante_cli',
                 color='recencia_meses',
                 title="Visualizador de clientes: Canal/Región/Clúster",

                 color_continuous_scale='thermal_r',
                 height=700)

# --------------------------------------------------------------------3D Scatter variables clúster (MG5)

mg5 = px.scatter_3d(df_cluster2, x="precio_promedio", y="avg_meses", z="visitas",
                    color="cluster_name",
                    size="constante_size",
                    opacity=1,
                    color_discrete_map={"Joly": "blue",
                                        "Bergeron": "green", "Coderre": "red"},
                    height=700, width=700,
                    title="Visualización variables de clústeres"
                    )
