from sklearn.cluster import KMeans

data=[[30],[35],[40],[80],[85],[90]]

model1 = KMeans(n_clusters=2,random_state=0,n_init=10)

model1.fit(data)

print("student groups: ")
print(model1.labels_)


