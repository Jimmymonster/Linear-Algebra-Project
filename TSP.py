import pandas as pd
import sys
# print(sys.getrecursionlimit())
sys.setrecursionlimit(5000)
# import data to list
# maybe use adjacency list later, adjacency matrix is bullshit
data=pd.read_excel('Input Data.xlsx')
l=data.values.tolist()
node = 8
alldist=[[] for i in range(node)]
for i in range(1,node+1):
    for k in range(node):
        alldist[k].append([])
    for j in range(1,node+1):
        if i==j or l[i][j]=='no data':
            for k in range(3):
                alldist[k][i-1].append(0)
        else:
            tmp=[float(k) for k in l[i][j].split(',')]
            for k in range(3):
                alldist[k][i-1].append(tmp[k])

# Traveling salesman problem solving part
# TSP brute force approach O(n!)
# Type 0=distance 1=time 2=cost 

needmark=0
ans=1e9
path=0
anspath=0
def TSPminimum(path,type,mark):
    global ans,anspath
    if (mark-needmark)&needmark==0:
        sum=0
        for i in range(0,len(path)-1):
            sum+=alldist[type][path[i]][path[i+1]]
        sum+=alldist[type][path[-1]][path[0]]
        if(ans==sum):
            anspath.append(path[:])
            anspath[-1].append(0)
        elif(ans>sum):
            ans=sum
            anspath=[]
            anspath.append(path[:])
            anspath[-1].append(0)
    for i in range(1,node):
        if mark & (1<<i):
            continue
        mark|=1<<i
        path.append(i)
        TSPminimum(path,type,mark)
        mark&=~(1<<i)
        path.pop()
def TSPmaximum(path,type,mark):
    global ans,anspath
    if (mark-needmark)&needmark==0:
        sum=0
        for i in range(0,len(path)-1):
            sum+=alldist[type][path[i]][path[i+1]]
        sum+=alldist[type][path[-1]][path[0]]
        if(ans==sum):
            anspath.append(path[:])
            anspath[-1].append(0)
        elif(ans<sum):
            ans=sum
            anspath=[]
            anspath.append(path[:])
            anspath[-1].append(0)
    for i in range(1,node):
        if mark & (1<<i):
            continue
        mark|=1<<i
        path.append(i)
        TSPmaximum(path,type,mark)
        mark&=~(1<<i)
        path.pop()
def findpath(need,type,max):
    global ans,path,anspath,needmark
    path=[0]
    anspath=[]
    needmark=0
    for i in need:
        needmark|= 1<<i
    if(max==0):
        ans=1e9
        TSPminimum(path,type,1)
    elif(max==1):
        ans=-1e9
        TSPmaximum(path,type,1)
    return ans,anspath

exportcell={'Path No': [],
            'Path' : [],
            'Type' : [],
            'Number' : [],
            'Min or Max' : [],
            'Need to visit' : [],
            'All place visited' : []}
idx=0
def insertcell(need,type,max):
    global idx
    tmp=findpath(need,type,max)
    for a in range(0,len(tmp[1])):
        s=""
        for b in tmp[1][a]:
            s+= l[b+1][0]+'-->'
        s=s[0:-3]
        exportcell['Path No'].append(idx)
        idx+=1
        exportcell['Path'].append(s)
        if(type==0):
            exportcell['Type'].append('Distance')
        elif(type==1):
            exportcell['Type'].append('Time')
        elif(type==2):
            exportcell['Type'].append('Cost')
        exportcell['Number'].append(tmp[0])
        if(max==0):
            exportcell['Min or Max'].append('Minimum')
        elif(max==1):
            exportcell['Min or Max'].append('Maximum')
        s=""
        for b in need:
            s+=l[b+1][0]+','
        s=s[0:-1]
        exportcell['Need to visit'].append(s)
        s=""
        for b in range(0,7):
            if b in need:
                s+=l[b+1][0]+','
        s=s[0:-1]
        exportcell['All place visited'].append(s)
def combination(i,st,mark,need):
    if(st>=2):
        insertcell(need,0,0)
        insertcell(need,0,1)
        insertcell(need,1,0)
        insertcell(need,1,1)
        insertcell(need,2,0)
        insertcell(need,2,1)
    for k in range(i,node):
        if(mark & 1<<k):
            continue
        mark |= 1<<k
        need.append(k)
        combination(k,st+1,mark,need)
        mark &= ~(1<<k)
        need.pop()
combination(0,0,0,[])
# print(exportcell)
data_export=pd.DataFrame(exportcell,columns=['Path No', 'Path' , 'Type' ,'Number' ,'Min or Max' , 'Need to visit' , 'All place visited' ])
data_export.to_excel(r'D:/KMITL/Year2 1st/Linear Algebra/Project/Export Data.xlsx',index=False,header=True)