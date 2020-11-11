# Importing all the required packages
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle

# Function Normalize
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


# ----------------------------------------------------------------------------- Importar df
df = pd.read_csv('data/offcorss_customer_202011011419_2.csv', sep=";")
#df = pd.read_csv('data/offcorss_customer_202011011353_overall.csv', sep=";") # COn la base completa

# reación de dos variables adicionales:
df["ran_meses"] = df["max_meses"]-df["min_meses"]
df["compras_x_visita"] = df["compras"] / df["visitas"]

# Transformación de variables:
df["ran_meses"] = df["max_meses"]-df["min_meses"]
df["compras_x_visita"] = df["compras"] / df["visitas"]

# Logs
df["precio_promedio_log"] = np.log(df["precio_promedio"]+1)
df["avg_meses_log"] = np.log(df["avg_meses"]+1)
df["compras_x_visita_log"] = np.log(df["compras_x_visita"]+1)
df["ticket_prom_compra_log"] = np.log(df["ticket_prom_compra"]+1)


# Aplicación del PCA sobre las variables seleccionadas:
para_pca = ["revenue", "visitas","compras"]

scaler = StandardScaler()
df_seg = scaler.fit_transform(df[para_pca])
pca = PCA()
pca.fit(df_seg)
pca = PCA(n_components = 1)
pca_df = pca.fit_transform(df_seg)
pca_df = pd.DataFrame(data = pca_df, columns = ["Dim1"])
scores_pca = normalize(pca_df)

# Separación del percentil 0.95 de la base para creación de clúster con mayores a dicho percentil:
df["score_pca"] = scores_pca
q95 = df["score_pca"].quantile(0.95)
df_may95 = df[df["score_pca"]> q95]
df_men95 = df[df["score_pca"]<= q95]

df_men95_norm = normalize(df_men95[["recencia", "revenue", "visitas","compras","precio_promedio_log", 
                        "ticket_prom_compra", "ticket_prom_compra_log",  "ran_meses", "avg_meses_log", 
                                    "avg_meses", "precio_promedio","compras_x_visita", "compras_x_visita_log"]])


# ----------------------------------------------------------- Aplicación del algoritmo
# Aplicación del k-means:
##import random
##random.seed(1234)
##k_clu = 3
##kmeans = KMeans(n_clusters=k_clu, init='k-means++')

# Apply & Predict
df2= df_men95_norm[["avg_meses", "precio_promedio"]]

kmeans = pickle.load(open("models/model.pkl", "rb"))
kmeans.fit(df2)
labels = kmeans.predict(df2)
centroids = kmeans.cluster_centers_


#----------------------- Sumas de cuadrados:
kmeans.inertia_

#--------------------------------------------------------------- Centroides
centroids = kmeans.cluster_centers_
df_centroides = pd.DataFrame(centroids)
df_centroides.columns = list(df2.columns)
df_centroides = df_centroides.transpose()

#--------------------------------------------------------------- Union de las bases y pegar clasificación de clústeres:
df_men95["cluster"] = labels
df_may95["cluster"] = "f"
df_cluster = df_men95.append(df_may95)

cluster_names = {0:"low_price ", 1:"medium_price", 2:"high_price", "f":"offcorss_fans"}
df_cluster["cluster_name"] = df_cluster["cluster"].map(cluster_names) 


# _____________________GRAFICOS DE MODELO _______________________________________________________________________________

# Modificaciones a df3 para graficar
df_cluster2 = df_cluster.copy()
df_cluster2["constante_cli"] = 1
df_cluster2["constante_size"] = 1
df_cluster2["recencia_meses"] = df_cluster2["recencia"] / 30



# -------------------------------------------------------------------Heatmap de centroides (MG2)
mg2 = px.imshow(df_centroides,
                labels=dict(x="Clúster"),
                title="Promedios normalizados de variables de clúster",
                width=500, height=400,
                color_continuous_scale='Cividis_r'
                )

# -------------------------------------------------------------------Scatter pares de variables (MG3)

mg3 = px.scatter(df_cluster2, x="recencia_meses",
                 y="avg_meses",
                 color="cluster_name",
                 title='Scatter pares de variables')

#-------------------------------------------------------------------------------- Treemap (MG4)

# Treemap clientes por canal/region/ciudad/cluster
mg4 = px.treemap(df_cluster2, path=[px.Constant('CLIENTES:  ' + str(df_cluster2["constante_cli"].sum())),
                                "canal_det", 'region',  "cluster_name"],
                 values='constante_cli',
                 color='recencia_meses',
                 title="Visualizador de clientes: Canal/Región/Clúster",

                 color_continuous_scale='thermal_r',
                 height=700)

# ------------------------------------------------------------------- 3D Scatter variables clúster (MG5)

mg5 = px.scatter_3d(df_cluster2, x="recencia_meses", y="avg_meses", z="visitas",
                    color="cluster_name",
                    size="constante_size",
                    opacity=1,
                    # size="revenue",
                    # hover_name="district", symbol="result",
                    color_discrete_map={"Joly": "blue",
                                        "Bergeron": "green", "Coderre": "red"},
                    height=500, width=600,
                    title="Visualización variables de clúster"
                    )
