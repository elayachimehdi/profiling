# Import library

import pandas as pd
from sklearn import preprocessing
from time import time
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from sklearn import cluster, metrics 
from time import time

import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn import decomposition
from sklearn import decomposition

# importer les jeux de données 
data=pd.read_csv('Dataset.csv')

# Traitement des données (traitement)
X = data.drop(7, axis=1).values
Y = data[7].values

# Normalisation des données

X_norm = preprocessing.scale(X)

# les K cluster 
#%matplotlib inline
#%pylab inline

silhouettes = []
for num_clusters in range (2, 10):
    cls = cluster.KMeans(n_clusters=num_clusters, 
                         n_init=1, init='random')
    cls.fit(X_norm)
    silh=metrics.silhouette_score(X_norm, cls.labels_)
    silhouettes.append(silh)

plt.plot(range(2, 10), silhouettes, marker='o')

# Clustering déterminer les K
pca = decomposition.PCA(n_components=2)
pca.fit(X_norm)
print(pca.explained_variance_ratio_)
X_trans = pca.transform(X_norm)

# Panel visualisation
fig = plt.figure(figsize=(12,5))
# 2 Clusters
cls = cluster.KMeans(n_clusters=2)
cls.fit=(X_norm)
ax = fig.add_subplot(121)
ax.scatter(X_trans[:, 0], X_trans[:, 1], c = cls.labels_)
# 3 Clusters 
cls3 = cluster.KMeans(n_clusters=3)
cls3.fit=(X_norm)
ax = fig.add_subplot(122)
ax.scatter(X_trans[:, 0], X_trans[:, 1], c = cls3.labels_)
 
# Comparaison 
fig = plt.figure(figsize=(12,5))

cls3 = cluster.KMeans(n_clusters=3)
cls3.fit=(X_norm)
ax = fig.add_subplot(121)
ax.scatter(X_trans[:, 0], X_tran[:, 1], c = cls3.labels_)

ax = fig.add_subplot(122)
ax.scatter(X_trans[:, 0], X_trans[:, 1], c=Y)

# performance 

print(metrics.adjusted_rand_score(Y, cls3.labels_))
