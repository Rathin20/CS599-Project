import random

no_nodes = 500
no_edges = 65000

nodes = [i for i in range(no_nodes)]
edges = [random.sample(nodes,2) for i in range(no_edges)]


with open('artificial_graph.txt', 'w') as f:
    for edge in edges:
        f.write(str(edge[0]) + ' ' + str(edge[1]))
        f.write('\n')
