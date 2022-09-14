import pandas as pd
from queue import PriorityQueue
import math
import time

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

# === TSP Part using DP ===
dp = [[-1]*(1 << (node)) for _ in range(node)]
def tsp(now,mark):
    #base case already go all place need
    if mark == (1<<(node))-1:
        return dist[now][0]
    if dp[now][mark] !=-1:
        return dp[now][mark]
    ans = 1e9
    for i in range(node):
        if(mark & (1<<i)==0):
            ans = min(ans,tsp(i,mark|(1<<i))+dist[now][i])
    dp[now][mark]=ans
    return ans

a=tsp(0,1)
print(a)
# Traceback Path
trace=[0]
mark=1
now=0
n=a
while len(trace)<node-1:
    ans=1e9
    next=0
    for i in range(node):
        if mark&(1<<i)==0 and dp[i][mark|(1<<i)]==n-dist[now][i]:
            next=i
            break
    trace.append(next)
    n-=dist[now][i]
    mark|=1<<next
    now=next
for i in range(node):
    if i not in trace:
        trace.append(i)
        trace.append(0)
        break
anspath=[0]
for i in range(len(trace)-1):
    anspath+=path[trace[i]][trace[i+1]][1:]
print(anspath)