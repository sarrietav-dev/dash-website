# Importing all the required packages
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import plotly.express as px
from sklearn.decomposition import PCA

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

# reación de dos variables adicionales:
df["ran_meses"] = df["max_meses"]-df["min_meses"]
df["compras_x_visita"] = df["compras"] / df["visitas"]

# Transformación de variables:
df["ran_meses_log"] = np.log(df["ran_meses"]+1)
df["fact_log"] = np.log(df["facturas_unicas"]+1)
df["visitas_log"] = np.log(df["visitas"]+1)
df["compras_log"] = np.log(df["compras"]+1)
df["reveune_log"] = np.log(df["revenue"]+1)
df["precio_promedio_log"] = np.log(df["precio_promedio"]+1)
df["ticket_log"] = np.log(df["ticket_prom_compra"]+1)
df["compras_x_visita_log"] = np.log(df["compras_x_visita"]+1)

# Seleccion de variables para modelo:
#numericas = [ "recencia", 'avg_meses', 'ran_meses_log', "visitas_log","precio_promedio_log", "ticket_log", "compras_x_visita_log"]
numericas = ['revenue', "ticket_prom_compra", "visitas"]
# Estas dan un accuracy de: XXX


con_outlier = ['visitas_log', 'precio_promedio_log',
               'ticket_log', 'compras_x_visita_log']
# Filtrar bottom 1% & top 1%.
low = .01
high = .99
quant_df = df[con_outlier].quantile([low, high])
df2 = df[con_outlier].apply(lambda x: x[(x >= quant_df.loc[low, x.name]) &
                                        (x < quant_df.loc[high, x.name])], axis=0)
df3 = pd.concat([df, df2], axis=1, join="inner")
df3 = df3.dropna()
df3 = df3.loc[:, ~df3.columns.duplicated()]

# ----------------------------------------------------------- Normalización de las variables seleccionadas:
df4 = normalize(df3[numericas])

# ----------------------------------------------------------- Aplicación del algoritmo
k = 4
kmeans = KMeans(n_clusters=k, init='k-means++')
kmeans.fit(df4)
df3["clusters"] = kmeans.labels_

# --------------------------------------------------------- Sumas de cuadrados:
kmeans.inertia_

#--------------------------------------------------------------- Centroides
centroids = kmeans.cluster_centers_
df_centroides = pd.DataFrame(centroids)
df_centroides.columns = list(df4[numericas])
df_centroides = df_centroides.transpose()


# ---------------------------------------------------------------- Para de PCA:

clu = df3["clusters"].reset_index()

pca = PCA(n_components=2)
pca_off = pca.fit_transform(df4[numericas])
pca_off_df = pd.DataFrame(data=pca_off, columns=["Dim1", "Dim2"])
pca_nombres = pd.concat([pca_off_df, clu["clusters"]], axis=1)


# _____________________GRAFICOS DE MODELO _______________________________________________________________________________

# Modificaciones a df3 para graficar
df3_mod = df3.copy()
df3_mod["clusters"] = df3_mod["clusters"].astype("string")
df3_mod["constante_cli"] = 1
df3_mod["constante_size"] = 1
df3_mod["recencia_meses"] = df3_mod["recencia"] / 30


# ------------------------------------------------------------------- Scatter de los PCA (MG1)
pca_nombres["clusters"] = pca_nombres["clusters"].astype(str)
mg1 = px.scatter(pca_nombres,
                 x="Dim1",
                 y="Dim2",
                 color="clusters",
                 title='Representación gráfica clusters')

# -------------------------------------------------------------------Heatmap de centroides (MG2)
mg2 = px.imshow(df_centroides,
                labels=dict(x="Clúster"),
                title="Promedios normalizados de variables de clúster",
                width=500, height=400,
                color_continuous_scale='Cividis_r'
                )

# -------------------------------------------------------------------Scatter pares de variables (MG3)

mg3 = px.scatter(df3_mod, x="recencia_meses",
                 y="avg_meses",
                 color="clusters",
                 title='Scatter pares de variables')

#-------------------------------------------------------------------------------- Treemap (MG4)

# Treemap clientes por canal/region/ciudad/cluster
mg4 = px.treemap(df3_mod, path=[px.Constant('CLIENTES:  ' + str(df3_mod["constante_cli"].sum())),
                                "canal_det", 'region', "ciudad", "clusters"],
                 values='constante_cli',
                 color='recencia_meses',
                 title="Visualizador de clientes",
                 color_continuous_scale='thermal_r',
                 height=700)

# ------------------------------------------------------------------- 3D Scatter variables clúster (MG5)

mg5 = px.scatter_3d(df3_mod, x="recencia_meses", y="avg_meses", z="visitas",
                    color="clusters",
                    size="constante_size",
                    opacity=1,
                    # size="revenue",
                    # hover_name="district", symbol="result",
                    color_discrete_map={"Joly": "blue",
                                        "Bergeron": "green", "Coderre": "red"},
                    height=500, width=600,
                    title="Visualización variables de clúster"
                    )
