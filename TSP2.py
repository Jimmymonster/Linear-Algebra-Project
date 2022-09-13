from asyncio.windows_events import NULL
import pandas as pd
from queue import Empty, PriorityQueue
import math

# === import data to list ===
data=pd.read_excel('Input Data2.xlsx','Car')
l=data.values.tolist()
node = len(l)
# === map node with number (easy to use) ===
key={}
for i in range(node):
    key[l[i][0]]=i
# === make adjacency list ===
dic={}
for i in l:
    now=""
    for j in i:
        if j==i[0]:
            now=j
            dic[key[now]]=[]
            continue
        if type(j) == str:
            tmp=j.split(',')
            dic[key[now]].append([key[tmp[0]],[float(k) for k in tmp[1:]]])
# print(dic)

# === dijkstra every node for allpair shortest path ===
dist=[[-1 for _ in range(node)] for _ in range(node)]
path=[[[j] for i in range(node)] for j in range(node)]
def dijkstra(node,type):
    global dist
    he=PriorityQueue()
    dist[node][node]=0
    he.put([0,node])
    while not he.empty():
        tmp=he.get()
        for i in dic[tmp[1]]:
            if dist[node][i[0]]==-1:
                dist[node][i[0]]=dist[node][tmp[1]]+i[1][type]
                path[node][i[0]]=path[node][tmp[1]]+[i[0]]
                he.put([i[1][type],i[0]])

for i in range(node):
    dijkstra(i,0)
# print(dist)
# print(path)

# === TSP Part DP ===