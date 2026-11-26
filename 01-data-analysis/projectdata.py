from sklearn.cluster import KMeans 

projects=[
    [5,10],
    [8,12],
    [6,15],
    [40,50],
    [45,55],
    [50,60],
    [10,18],
    [42,48]
]

model=KMeans(n_clusters=2,random_state=0,n_init=10)

model.fit(projects)

print("software project analysis")

for i in range(len(projects)):
    print("project",i+1,
          "bugs:",projects[i][0],
          "days:",projects[i][1],
          "groups:",model.labels_[i]
          )
