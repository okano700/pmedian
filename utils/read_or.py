import urllib.request
import numpy as np
from scipy.sparse.csgraph import floyd_warshall

def read_or_library(url, def_value = 999):
  with urllib.request.urlopen(url) as f:
    html = f.read().decode('utf-8')
  data = html.split('\n')
  clean_data = []
  for i in data:
    clean_data.append(i.strip().split(' '))
  a = [[def_value for i in range(int(clean_data[0][0]))] for j in range(int(clean_data[0][0]))]
  for i in range(1,int(clean_data[0][1])+1):
    a[int(clean_data[i][0])-1][int(clean_data[i][1])-1] = int(clean_data[i][2])
    a[int(clean_data[i][1])-1][int(clean_data[i][0])-1] = int(clean_data[i][2])
  for i in range(int(clean_data[0][0])):
    a[i][i] = 0

  a = floyd_warshall(a)
  print('numero de vertices')
  print(clean_data[0][0])
  print('numero de arestas')
  print(clean_data[0][1])
  print('p')
  print(clean_data[0][2])
  return np.array(a), int(clean_data[0][2]), int(clean_data[0][0])
