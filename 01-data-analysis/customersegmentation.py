from sklearn.cluster import KMeans

data = [[1000],[1200],[1500],[8000],[8500],[9000]]

model = KMeans(n_clusters=2,random_state=0,n_init=10)

model.fit(data)

print("customer groups: ")
print(model.labels_)

