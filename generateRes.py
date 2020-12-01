from utils.read_or import read_or_library
from utils.VNS import VNS
import pandas as pd
from tqdm import trange

data = pd.read_csv('dataset/pmed.csv',sep=',')

res = []
for index, row in data.iterrows():
  best_solution = int(row[1])
  print(row[0])
  A, p, v = read_or_library('http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/'+row[0]+'.txt',999)
  s0 = [i for i in range(int(p))]
  results = []
  for i in trange(10):
    out = {}
    sol, fo, log,time = VNS(A,list(s0),5,20,max_time= 600, opt = best_solution)
    out['time'] = time
    out['fo'] = fo
    results.append(out)
  save = pd.DataFrame(results)
  save.to_csv('results/'+row[0]+'.csv')
