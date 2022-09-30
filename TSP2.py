import pandas as pd
from queue import PriorityQueue
import math
import time
exportcell={'Path No': [],
            'Path' : [],
            'Type' : [],
            'Minimum Value' : [],
            'Need to visit' : [],
            'All value(dist,time,cost)' : [],
            'All place visited' : []}

# === import data to list ===
data=pd.read_excel('Input Data.xlsx','Car')
l=data.values.tolist()
node = len(l)
# === map node with number (easy to use) ===
key={}
for i in range(node):
    key[l[i][0]]=i
    key[i]=l[i][0]
# === make adjacency list ===
dic={}
for i in l:
    now=""
    for j in i:
        if j==i[0]:
            now=j
            dic[key[now]]=[]
            continue
        elif type(j) == str:
            tmp=j.split(',')
            dic[key[now]].append([key[tmp[0]],[float(k) for k in tmp[1:]]])
# print(dic)

# === dijkstra every node for allpair shortest path ===
dist=[[1e9 for _ in range(node)] for _ in range(node)]
dist2=[[1e9 for _ in range(node)] for _ in range(node)]
dist3=[[1e9 for _ in range(node)] for _ in range(node)]
path=[[[j] for i in range(node)] for j in range(node)]
def dijkstra(node,type):
    global dist
    he=PriorityQueue()
    dist[node][node]=0
    dist2[node][node]=0
    dist3[node][node]=0
    he.put([0,node])
    while not he.empty():
        tmp=he.get()
        for i in dic[tmp[1]]:
            if dist[node][i[0]]>dist[node][tmp[1]]+i[1][type]:
                dist[node][i[0]]=dist[node][tmp[1]]+i[1][type]
                dist2[node][i[0]]=dist2[node][tmp[1]]+i[1][(type+1)%3]
                dist3[node][i[0]]=dist3[node][tmp[1]]+i[1][(type+2)%3]
                path[node][i[0]]=path[node][tmp[1]]+[i[0]]
                he.put([i[1][type],i[0]])

# === TSP Part using DP ===
dp = [[-1]*(1 << (node)) for _ in range(node)]
def tsp(now,mark,need):
    global dist
    #base case already go all place need
    if mark & need == need:
        return dist[now][0]
    if dp[now][mark] !=-1:
        return dp[now][mark]
    ans = 1e9
    for i in range(node):
        if(mark & (1<<i)==0):
            ans = min(ans,tsp(i,mark|(1<<i),need)+dist[now][i])
    dp[now][mark]=ans
    return ans

# for i in range(node):
#     dijkstra(i,0)
# print(tsp(0,1,3))
# dp = [[-1]*(1 << (node)) for _ in range(node)]
# print(tsp(0,1,5))

# combination
idx=0
def play(type):
    global dist,path,dp,dist2,dist3
    dist=[[1e9 for _ in range(node)] for _ in range(node)]
    dist2=[[1e9 for _ in range(node)] for _ in range(node)]
    dist3=[[1e9 for _ in range(node)] for _ in range(node)]
    path=[[[j] for i in range(node)] for j in range(node)]
    for i in range(node):
        dijkstra(i,type)
    for need in range(3,(1<<(node)),2):
        # print("{0:b}".format(need))
        dp = [[-1]*(1 << (node)) for _ in range(node)]
        mincost=tsp(0,1,need)
        # print(mincost)

        # === Traceback Path ===
        trace=[0]
        mark=1
        now=0
        cou=1
        n=mincost
        while cou<node-1:
            ans=1e9
            next=0
            for i in range(node):
                if mark&(1<<i)==0 and dp[i][mark|(1<<i)]==n-dist[now][i]:
                    next=i
                    break
            if next!=0:
                trace.append(next)
            cou+=1
            n-=dist[now][i]
            mark|=1<<next
            now=next
        for i in range(node):
            if i not in trace and (1<<i)&need!=0:
                trace.append(i)
                break
        trace.append(0)
        # print(trace)
        anspath=[0]
        for i in range(len(trace)-1):
            anspath+=path[trace[i]][trace[i+1]][1:]
        # print(anspath)

        # === insert to cell ===
        global idx
        s=""
        exportcell['Path No'].append(idx)
        idx+=1
        for i in anspath:
            s+=key[i]+'-->'
        s=s[0:-3]
        exportcell['Path'].append(s)
        if(type==0):
            exportcell['Type'].append('Distance')
        elif(type==1):
            exportcell['Type'].append('Time')
        elif(type==2):
            exportcell['Type'].append('Cost')
        exportcell['Minimum Value'].append(mincost)
        s=""
        for i in range(0,node):
            if (1<<i)&need!=0:
                s+=key[i]+','
        s=s[0:-1]
        exportcell['Need to visit'].append(s)
        s=""
        d=[0,0,0]
        for i in range(0,len(anspath)-1):
            d[type]+=dist[anspath[i]][anspath[i+1]]
            d[(type+1)%3]+=dist2[anspath[i]][anspath[i+1]]
            d[(type+2)%3]+=dist3[anspath[i]][anspath[i+1]]
        s= "{:g}".format(d[0])+","+"{:g}".format(d[1])+","+"{:g}".format(d[2])
        exportcell['All value(dist,time,cost)'].append(s)
        s=""
        for i in range(0,node):
            if i in anspath:
                s+=key[i]+','
        s=s[0:-1]
        exportcell['All place visited'].append(s)

play(0)
play(1)
play(2)
data_export=pd.DataFrame(exportcell,columns=['Path No', 'Path' , 'Type' ,'Minimum Value' , 'Need to visit' , 'All value(dist,time,cost)','All place visited' ])
data_export.to_excel(r'../Project/Export Data.xlsx',index=False,header=True)