from sklearn.datasets import load_iris
from sklearn.cluster import KMeans

iris = load_iris()
kmeans = KMeans(n_clusters=3)

kmeans.fit(iris.data)
cluster_labels = kmeans.labels_

print("Cluster Labels:", cluster_labels)