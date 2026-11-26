from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
x=np.array([
    [5,80,75],
    [6,85,80],
    [2,50,40],
    [8,90,90],
    [3,60,50]
])

Scaler = StandardScaler()
x_scaled = Scaler.fit_transform(x)

pca=PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)

print("Original Data: ")
print(x)

print("data after PCA: ")
print(x_pca)
