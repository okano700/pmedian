from tqdm import tnrange, tqdm_notebook
import tqdm
import numpy as np
import time


def get_cost(A,C):
  """
  A = matriz de adjacencia
  C = Soluçao a ser calculado o custo
  """
  aux = A[:,C]
  y = np.argmin(aux,axis = 1)
  fo = 0
  for i in range(len(y)):
    fo += aux[i,y[i]]

  return fo

def shuffle_neighbor(A,S,n, max = 999):
  """
  A = matriz de adjacencia
  S = Solução
  n = numero de pontos para cada mediana
  """
  sSol = len(S)
  aux = [A[:,i].argsort()[:n][::1] for i in S]
  aux = np.array(aux)
  """
  opt = []
  for i in range(len(S)):
    v = []
    for j in range(len(aux[i])):
      if A[S[i]][aux[i][j]] != max:
        v.append(aux[i][j])
    opt.append(np.array(v))
  opt = np.array(opt)
  aux = opt
  """
  for i in range(len(S)):
    S[i] = np.random.choice(aux[i])

  return S

def get_neighbor(A,S,n):
  """
  A = matriz de adjacencia
  S = Solução
  n = numero de pontos para cada mediana
  """
  sSol = len(S)
  aux = [A[:,i].argsort()[:n][::1] for i in S]
  aux = np.array(aux)
  cost = get_cost(A,S)
  Saux = list(S)
  auxCost = get_cost(A,Saux)
  ind = [i for i in range(len(S))]
  np.random.shuffle(ind)
  for i in ind:
    Saux = list(S)
    for j in range(len(aux[i])):
      if aux[i][j]  not in Saux:
        Saux[i] = aux[i][j]
        auxCost = get_cost(A,Saux)
      if auxCost < cost:
        cost = auxCost
        S = list(Saux)

  return S




def best_improvement(A,S,n):
  """
  A = matriz de adjacencia
  S = Solução
  n = numero de pontos para cada mediana
  """
  Sol = get_neighbor(A,S,n)
  val = [get_cost(A,i) for i in Sol]
  return Sol[np.argmin(val)]

def first_improvement(A,S,n):
  """
  A = matriz de adjacencia
  S = Solução
  n = numero de pontos para cada mediana
  """
  s = get_cost(A,S)
  Sol = get_neighbor(A,S,n)
  #np.random.shuffle(Sol)

  nS = S

  for i in Sol:

    if get_cost(A,i)< s:
      nS = i
      break

  return nS


def VNS(A,s0,k0,kmax,max_time = 600, opt = None):
  s = s0
  fs = get_cost(A,s)
  start = time.perf_counter()
  log = []
  log.append(fs)
  now = time.perf_counter()
  while now < start + max_time:
    k = k0
    while k <= kmax:
      randomNeighbor = shuffle_neighbor(A,list(s),k)
      ns= get_neighbor(A,list(randomNeighbor),k)
      fns = get_cost(A,ns)
      if fns < fs:
        s = ns
        fs = fns
        k = k0
      else:
        k+= 1
      log.append(fs)
      if (opt != None) and (fs == opt):
        break
    if (opt != None) and (fs == opt):
      break
    now = time.perf_counter()
  return s, fs, log, (now-start)
