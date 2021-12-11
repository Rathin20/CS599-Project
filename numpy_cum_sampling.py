from read_file import adj_list
import numpy as np
import random
import time
import sys
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
length = int(106349211*0.03)
d_E = np.zeros(length)

#Defining Functions

def random_neighbour(node):
  return random.sample(adj_list[node],1)[0]

'''
def random_walk(node,length):				#What to do when it node -> node1 -> node2 -> node happens and node2 has only node as an edge?
	list_of_nodes = [node]
	R = []
	i = 0
	while i<length:
		neighbour = random_neighbour(node)
		if neighbour not in list_of_nodes:
			R.append((node,neighbour))
			list_of_nodes.append(neighbour)
			node = neighbour
			i = i + 1
	return R
'''
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
  if max(len(adj_list[edge[0]]),len(adj_list[edge[0]])) < len(adj_list[node]):
    return True
  else:
    return False

'''
def collisions(edge_list):
  c = 0
  for i in range(len(edge_list)):
      for j in range(i+1,len(edge_list)):
          if edge_list[i] == edge_list[j]:
#            print(str(edge_list[i]))+ str(" ") + str(edge_list[j])
            c = c + 1
  return c


def edge_count_estimator(R,mix):    #c_i can be improved
  R_mix = [[] for x in range(mix)]
  c_i   = [0.0 for x in range(mix)]
  Y_i   = [0.0 for x in range(mix)]
  Y     = 0.0 
  for i in range(mix):
    for j in range(i,len(R),mix):
        R_mix[i].append(R[j])
    c_i[i] = collisions(R_mix[i])
    Y_i[i] = len(R_mix[i])*(len(R_mix[i])-1)/2*float(c_i[i])
    Y = Y + Y_i[i]
  return Y/mix
'''

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
    Y = Y + R_sub[i][0]*(R_sub[i][0]-1.0)/(2.0*R_sub[i][1])

  return Y/mix

def tetris(s,r,l,mix):
  Y = 0
  R = random_walk(s,r)
  start = time.process_time()
  edges = sample_edges(R,l)
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
    print("Checking " + str(time.process_time() - asso))
  Y = Y/l
  print("Y is " + str(Y) )
  m = edge_count_estimator(R,mix)
  print("m is " + str(m))
  X =(m/r)*d_R*Y
  print("d_R is " + str(d_R))
  return X

start = time.process_time()
tr = tetris(4,length,int(0.05*length),int(sys.argv[1]))
time_needed = time.process_time() - start
print("Mixing time is " + str(sys.argv[1]) + "\n")
print("Triangles are " + str(tr))

f = open("plot.txt",'a')
f.write(str(sys.argv[1])+","+str(tr)+ "," + str(time_needed)+"\n")
f.close()
