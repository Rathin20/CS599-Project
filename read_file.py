import sys
adj_list  = {}
mylist    = []

def add_node(node):
  if node not in mylist:
    mylist.append(int(node))

def add_in_adj_list(edge):
  x, y = list(map(int, edge))
  for u, v in [(x, y), (y, x)]:
    if u not in adj_list:
      adj_list[u] = []
    adj_list[u].append(v)


with open("soc-orkut.txt") as file:
  read_line_count = 0
  while True:
    if read_line_count > 3:
      line = file.readline()
      if not line:
        break
      else:
        edge = line.strip().split()
        add_in_adj_list(edge)
        read_line_count = read_line_count + 1
        if read_line_count % 1000000 == 0:
            print("{} lines done".format(read_line_count))
    else:
      line = file.readline()
      read_line_count = read_line_count + 1
