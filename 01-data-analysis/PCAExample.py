from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
x=np.array([
  [2,4],
  [3,6],
  [4,8],
  [5,10],
  [6,12]
 ])
Scaler = StandardScaler()
x_scaled = Scaler.fit_transform(x)

pca = PCA(n_components=1)
x_pca = pca.fit_transform(x_scaled)

print("Original Data: ")
print(x)

print("data after PCA: ")
print(x_pca)

''' FINAL EXAM IMP* TOPIC
knowledge representation,rulbased ,recommendation,
rainforesment , staming , tokenlization,inroduction to chatbos deplopment,
introduction to cv,test pre processing , decision tree'''
