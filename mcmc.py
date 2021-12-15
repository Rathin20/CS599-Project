from read_file import adj_list
import numpy as np
import random
import time
import sys
#from generate import nodes,edges
#graph = [[1,2],[2,3],[1,3],[4,5],[10,23],[4,6],[2,6],[2,4]]
'''
adj_list = {
  1: [2,3],
  2: [1,3,4,6],
  3: [1,2],
  4: [2,5,6],
  5: [4,6,10],
  6: [2,4,5],
  10: [5,23],
  23: [5,10]
}
'''

#Global Variables
d_R = 0.0
length = int(0.75*88236)
d_E = np.zeros(length)

#Defining Functions

def random_neighbour(node):
  return random.sample(adj_list[node],1)[0]

def edge_degree(e):
    return min(len(adj_list[e[0]]),len(adj_list[e[1]]))


def random_walk(node,length):
    R = np.zeros((length,2))
    global d_E
    global d_R
    i = 0
    while i<length:
        neighbour = random_neighbour(node)
        R[i] = (node,neighbour)
        d_E[i] = float(edge_degree((node,neighbour)))
        d_R = d_R + d_E[i]
        node = neighbour
        i = i + 1
    d_E = d_E/d_R
    return R

def sample_edges(R,l):
    return random.choices(R,d_E,k=l)


def check_triangle(edge,node):
  if node in adj_list[edge[0]] and node in adj_list[edge[1]]:
    return True
  else:
    return False

def check_association(edge, node):
  if max(len(adj_list[edge[0]]),len(adj_list[edge[0]])) <= len(adj_list[node]):
    return True
  else:
    return False

def collisions(n):
  if n == 1:
      return 0
  else:
      return n*(n-1)/2

def edge_count_estimator(R,mix):
  counts = []
  R_sub = []
  Y = 0.0
  start = time.process_time()
  for i in range(mix):
      print(i)
      counts.append(np.unique(R[i:len(R):mix],axis = 0, return_counts = True))
  print("Done counts " + str(time.process_time() - start))

  coll = time.process_time()
  for i in range(len(counts)):
    R_sub.append((len(R[i:len(R):mix]),np.sum(np.asarray(list(map(collisions,counts[i][1]))))))
  print ("Done collisions " + str(time.process_time()-coll))

  for i in range(len(R_sub)):
    if R_sub[i][1] > 0.0:
      Y = Y + R_sub[i][0]*(R_sub[i][0]-1.0)/(2.0*R_sub[i][1])
  return Y/mix

def tetris(s,r,l,mix,R):
  Y = 0
  start = time.process_time()
  edges = sample_edges(R,l)
  print(edges[0])
  print("Sampling " + str(time.process_time()-start))
  for i in range(l):
    asso = time.process_time()
    if len(adj_list[edges[i][0]]) < len(adj_list[edges[i][1]]):
      w = random_neighbour(edges[i][0])
    else:
      w = random_neighbour(edges[i][1])
    if check_triangle(edges[i],w) == True:
      if check_association(edges[i],w) == True:
        Y = Y + 1
  Y = Y/l
  print("Y is " + str(Y) )
  m = edge_count_estimator(R,mix)
  print("m is " + str(m))
  X =(m/r)*d_R*Y
  print("d_R is " + str(d_R))
  return X


def mcmc(s,r,l,mix,R):
  Y = 0
#  R = random_walk(s,r)
  for i in range(len(R)):
    for j in range(2):
        print(i)
        neighbour0 = random_neighbour(R[i][j])
        neighbour1 = random_neighbour(R[i][j])
        if check_triangle((neighbour0,neighbour1),R[i][j]) == True:
          Y = Y + 1

  print("MCMC Y is" + str(Y/(l)))
  m = edge_count_estimator(R,mix)
  print("MCMC m is" + str(m))
  X =(m/r)*d_R*(Y/l)
  return X



s=0
r=length
R = random_walk(s,r)

'''
start_cn = time.process_time()
cn_tr = chiba_nishizeki(nodes,edges)
time_needed_cn = time.process_time() - start_cn
print(cn_tr)
'''

start_mcmc = time.process_time()
mcmc_tr = mcmc(0,length,int(0.05*length),75,R)
time_needed_mcmc = time.process_time() - start_mcmc

start_tetris = time.process_time()
tetris_tr = tetris(0,length,int(0.05*length),75,R)
time_needed_tr = time.process_time() - start_tetris


f = open("plot.txt",'a')
#f.write(str(len(edges))+","+str(cn_tr)+ "," + str(time_needed_cn)+ "," + str(mcmc_tr)+ "," + str(time_needed_mcmc) + "," + str(tetris_tr)+ "," + str(time_needed_tr)+ "\n")
f.write( str(mcmc_tr)+ "," + str(time_needed_mcmc) + "," + str(tetris_tr)+ "," + str(time_needed_tr)+ "\n")

f.close()
