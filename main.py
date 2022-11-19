import tkinter as tk
from tkinter import VERTICAL, Scrollbar, StringVar, ttk
# from turtle import width
# from typing import Container
# from tkinter import *
import pandas as pd
# import numpy as np
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
# import openpyxl
from queue import PriorityQueue
# Global Var
bg='black'
frame_bg='black'

font='TH Sarabun New'
font_header_size=40
font_body_size=20
font_table_size=15
font_col='white'

# === map node with number (easy to use) ===
inputdata=pd.read_excel('Input Data.xlsx','Sheet1')
l=inputdata.values.tolist()
key={}
node = len(l)
for i in range(node):
    key[l[i][0]]=i
    key[i]=l[i][0]
#============================================
exportdata=pd.read_excel('Export Data.xlsx')
l=exportdata.values.tolist()
allplace=l[-1][-3].split(',')
chboxVar={}
chbox=[0]
#============================ Calculate ==============================
def findPearson(first,firstmean,second,secondmean):
    uppersum=0 # fraction in pearson similarity formular
    below1=0 # first denominator in pearson similarity formular
    below2=0 # second denominator in pearson similarity formular
    for k in range(len(first)):
        uppersum+=(first[k]-firstmean)*(second[k]-secondmean)
        below1+= (first[k]-firstmean)**2
        below2+= (second[k]-secondmean)**2
    if ((below1*below2)**0.5)==0: return 1.0
    return uppersum/((below1*below2)**0.5)
def findCosine(first,second):
    uppersum=0 # fraction in cosine similarity formular
    below1=0 # first denominator in cosine similarity formular
    below2=0 # second denominator in cosine similarity formular
    for k in range(len(first)):
        uppersum+=first[k]*second[k]
        below1+=first[k]**2
        below2+=second[k]**2
    return uppersum/((below1*below2)**0.5)
def chvisited(datarow,tarvisited):
    tmpvisit=0
    for j in l[datarow][6].split(','):
        tmpvisit|=1<<key[j]
    if(tarvisited&tmpvisit==tarvisited): return True
    else: return False

def calculate():
    needtogo=1
    oneset=(int(l[-1][0])+1)//3
    for i in range(1,len(allplace)):
        needtogo|=chboxVar[allplace[i]].get()<<i
    # print(l[(needtogo-3)//2]) # Distance
    # print(l[((needtogo-3)//2)+oneset]) # Time
    # print(l[((needtogo-3)//2)+oneset+oneset]) # Cost
    visited=[0,0,0] #target visited [bestof Dis, bestof Time, bestof Cost]
    mean=[0,0,0] #target mean [bestof Dis, bestof Time, bestof Cost]
    for i in l[(needtogo-3)//2][6].split(','):
        visited[0]|=1<<key[i]
    for i in l[((needtogo-3)//2)+oneset][6].split(','):
        visited[1]|=1<<key[i]
    for i in l[((needtogo-3)//2)+oneset+oneset][6].split(','):
        visited[2]|=1<<key[i]
    dtar=[float(_) for _ in l[(needtogo-3)//2][5].split(',')]
    mean[0]=sum(dtar)/3
    ttar=[float(_) for _ in l[((needtogo-3)//2)+oneset][5].split(',')]
    mean[1]=sum(ttar)/3
    ctar=[float(_) for _ in l[((needtogo-3)//2)+oneset+oneset][5].split(',')]
    mean[2]=sum(ctar)/3
    # print(mean)
    pqDpearson=PriorityQueue() # [Pearson similarity value , index] max heap
    pqTpearson=PriorityQueue() # [Pearson similarity value , index] max heap
    pqCpearson=PriorityQueue() # [Pearson similarity value , index] max heap
    pqDcosine=PriorityQueue() # [Cosine similarity value , index] max heap
    pqTcosine=PriorityQueue() # [Cosine similarity value , index] max heap
    pqCcosine=PriorityQueue() # [Cosine similarity value , index] max heap
    # for cov Matrix
    sumDis=[0,0,0]
    sumTime=[0,0,0]
    sumCost=[0,0,0]
    matDis=[[0 for i in range(3)] for j in range(oneset)]
    matTime=[[0 for i in range(3)] for j in range(oneset)]
    matCost=[[0 for i in range(3)] for j in range(oneset)]
    covDis=[[0 for i in range(3)] for j in range(3)]
    covTime=[[0 for i in range(3)] for j in range(3)]
    covCost=[[0 for i in range(3)] for j in range(3)]
    for i in range(oneset):
        d=[float(_) for _ in l[i][5].split(',')]
        t=[float(_) for _ in l[i+oneset][5].split(',')]
        c=[float(_) for _ in l[i+oneset+oneset][5].split(',')]
        if(chvisited(i,visited[0])):
            dmean=sum(d)/3
            pqDpearson.put([-findPearson(dtar,mean[0],d,dmean),i])
            pqDcosine.put([-findCosine(dtar,d),i])
        if(chvisited(i+oneset,visited[1])):
            tmean=sum(t)/3
            pqTpearson.put([-findPearson(ttar,mean[1],t,tmean),i+oneset])
            pqTcosine.put([-findCosine(ttar,t),i+oneset])
        if(chvisited(i+oneset+oneset,visited[2])):
            cmean=sum(c)/3
            pqCpearson.put([-findPearson(ctar,mean[2],c,cmean),i+oneset+oneset])
            pqCcosine.put([-findCosine(ctar,c),i+oneset+oneset])
        for j in range(3):
            sumDis[j]+=d[j]
            matDis[i][j]=d[j]
            sumTime[j]+=t[j]
            matTime[i][j]=t[j]
            sumCost[j]+=c[j]
            matCost[i][j]=c[j]
    for i in range(oneset):
        for j in range(3):
            matDis[i][j]-=sumDis[j]/oneset
            matTime[i][j]-=sumTime[j]/oneset
            matCost[i][j]-=sumCost[j]/oneset
    for i in range(oneset):
        for j in range(3):
            for k in range(3):
                covDis[j][k]+=matDis[i][j]*matDis[i][k]
                covTime[j][k]+=matTime[i][j]*matTime[i][k]
                covCost[j][k]+=matCost[i][j]*matCost[i][k]
    for i in range(3):
        for j in range(3):
            covDis[i][j]/=oneset
            covTime[i][j]/=oneset
            covCost[i][j]/=oneset
    return pqDpearson,pqTpearson,pqCpearson,pqDcosine,pqTcosine,pqCcosine,covDis,covTime,covCost

#============================= All Page ==============================
class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    
    def __init__(self, master):
        #=======================================================
        # Dijkstra and TSP
        exportcell={'Path No': [],
            'Path' : [],
            'Type' : [],
            'Minimum Value' : [],
            'Need to visit' : [],
            'All value(dist,time,cost)' : [],
            'All place visited' : []}

        # === import data to list ===
        data=pd.read_excel('Input Data.xlsx','Sheet1')
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
        self.dist=[[1e9 for _ in range(node)] for _ in range(node)]
        self.dist2=[[1e9 for _ in range(node)] for _ in range(node)]
        self.dist3=[[1e9 for _ in range(node)] for _ in range(node)]
        self.path=[[[j] for i in range(node)] for j in range(node)]
        def dijkstra(node,type):
            he=PriorityQueue()
            self.dist[node][node]=0
            self.dist2[node][node]=0
            self.dist3[node][node]=0
            he.put([0,node])
            while not he.empty():
                tmp=he.get()
                for i in dic[tmp[1]]:
                    if self.dist[node][i[0]]>self.dist[node][tmp[1]]+i[1][type]:
                        self.dist[node][i[0]]=self.dist[node][tmp[1]]+i[1][type]
                        self.dist2[node][i[0]]=self.dist2[node][tmp[1]]+i[1][(type+1)%3]
                        self.dist3[node][i[0]]=self.dist3[node][tmp[1]]+i[1][(type+2)%3]
                        self.path[node][i[0]]=self.path[node][tmp[1]]+[i[0]]
                        he.put([i[1][type],i[0]])

        # === TSP Part using DP ===
        self.dp = [[-1]*(1 << (node)) for _ in range(node)]
        def tsp(now,mark,need):
            #base case already go all place need
            if mark & need == need:
                return self.dist[now][0]
            if self.dp[now][mark] !=-1:
                return self.dp[now][mark]
            ans = 1e9
            for i in range(node):
                if(mark & (1<<i)==0):
                    ans = min(ans,tsp(i,mark|(1<<i),need)+self.dist[now][i])
            self.dp[now][mark]=ans
            return ans

        # for i in range(node):
        #     dijkstra(i,0)
        # print(tsp(0,1,3))
        # dp = [[-1]*(1 << (node)) for _ in range(node)]
        # print(tsp(0,1,5))

        # combination
        self.idx=0
        def play(type):
            self.dist=[[1e9 for _ in range(node)] for _ in range(node)]
            self.dist2=[[1e9 for _ in range(node)] for _ in range(node)]
            self.dist3=[[1e9 for _ in range(node)] for _ in range(node)]
            self.path=[[[j] for i in range(node)] for j in range(node)]
            for i in range(node):
                dijkstra(i,type)
            for need in range(3,(1<<(node)),2):
                # print("{0:b}".format(need))
                self.dp = [[-1]*(1 << (node)) for _ in range(node)]
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
                        if mark&(1<<i)==0 and self.dp[i][mark|(1<<i)]==n-self.dist[now][i]:
                            next=i
                            break
                    if next!=0:
                        trace.append(next)
                    cou+=1
                    n-=self.dist[now][i]
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
                    anspath+=self.path[trace[i]][trace[i+1]][1:]
                # print(anspath)

                # === insert to cell ===
                s=""
                exportcell['Path No'].append(self.idx)
                self.idx+=1
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
                    d[type]+=self.dist[anspath[i]][anspath[i+1]]
                    d[(type+1)%3]+=self.dist2[anspath[i]][anspath[i+1]]
                    d[(type+2)%3]+=self.dist3[anspath[i]][anspath[i+1]]
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
        data_export.to_excel(r'Export Data.xlsx',index=False,header=True)
        self.reset()
        #=========================================================
        tk.Frame.__init__(self,master,bg=frame_bg)
        tk.Label(self, text="เลือกสถานที่ที่คุณอยากจะไป เราจะเลือกเส้นทางที่ดีที่สุดให้คุณ", font=(font,font_header_size), fg=font_col,bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)
        tk.Label(self, text=allplace[0] + " จุดเริ่มต้น ",font={font,font_body_size}, fg=font_col,bg=frame_bg).pack(padx=0,pady=5,side=tk.TOP)
        for i in range(1,len(allplace)):
            chboxVar[allplace[i]]=tk.IntVar()
            chbox.append(tk.Checkbutton())
            chbox[i]=tk.Checkbutton(self,text=allplace[i],variable=chboxVar[allplace[i]],font={font,font_body_size},fg=font_col,bg=frame_bg,activebackground=frame_bg,activeforeground=font_col,selectcolor=frame_bg)
            chbox[i].pack(padx=0,pady=5,side=tk.TOP)

        err = tk.Label(self, text="เลือกสักที่สิ", font=(font,font_header_size), fg="black",bg=frame_bg)
        err.pack(padx=0, pady=20, side=tk.TOP)
        tk.Button(self, text='ใส่ข้อมูลเส้นทาง', font=(font, font_body_size),width=20, height=1,command=lambda: master.switch_frame(InputPage)).pack(padx=120, pady=20, side=tk.LEFT)
        tk.Button(self, text='เริ่มคำนวนเส้นทาง', font=(font, font_body_size),width=20, height=1,command=lambda: master.switch_frame(ResultPage) if(self.check()) else err.config(fg="red")).pack(padx=0, pady=20, side=tk.TOP)
    # check if every items is not select
    def check(self):
        ch=False
        for i in range(1,len(allplace)):
            if(chboxVar[allplace[i]].get()):
                ch=True
        return ch
    def reset(self):
        global inputdata,l,key,node
        inputdata=pd.read_excel('Input Data.xlsx','Sheet1')
        l=inputdata.values.tolist()
        key={}
        node = len(l)
        for i in range(node):
            key[l[i][0]]=i
            key[i]=l[i][0]
        #========================================
        global allplace,chboxVar,exportdata,chbox
        exportdata=pd.read_excel('Export Data.xlsx')
        l=exportdata.values.tolist()
        allplace=l[-1][-3].split(',')
        chboxVar={}
        chbox=[0]
        #========================================
        
class InputPage(tk.Frame):
    
    def __init__(self,master):
        self.Containers=[]
        self.inputxts=[]

        tk.Frame.__init__(self,master,bg=frame_bg)

        TOPFrame=tk.Frame(self,width="1600",height="500", relief='raised',bg=frame_bg)
        TOPFrame.pack(padx=20,pady=20,fill=tk.BOTH,expand=True)
        TOPFrame.pack_propagate(0)

        self.my_canvas= tk.Canvas(TOPFrame,bg=frame_bg,highlightbackground="black")
        self.my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        
        self.scroll= ttk.Scrollbar(TOPFrame,orient=VERTICAL,command=self.my_canvas.yview)
        self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
        # style=ttk.Style()
        # style.theme_use('classic')
        # style.configure("Vertical.TScrollbar",troughcolor="black")

        self.my_canvas.configure(yscrollcommand=self.scroll.set)
        self.my_canvas.bind('<Configure>',lambda e:self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

        self.Con= tk.Frame(self.my_canvas,bg=frame_bg)
        
        self.my_canvas.create_window((0,0),window=self.Con,anchor="nw")

        Container = tk.Frame(self.Con,bg=frame_bg,height="3",width="1600")
        Container.pack(padx=5,pady=5,side=tk.TOP)
        tk.Label(Container,text='ชื่อจุดเริ่มต้น : ', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
        self.startinp= tk.Text(Container,height = 1,width = 20)
        self.startinp.pack(side=tk.LEFT)
        
        Container = tk.Frame(self.Con,bg=frame_bg,height="3",width="1600")
        inputtxt = [tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20)]
        for i in range(5):
            if(i==0):
                tk.Label(Container,text='เส้นทางจาก', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            inputtxt[i].pack(padx=20,pady=20, side=tk.LEFT)
            if(i==0):
                tk.Label(Container,text=' --> ', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            if(i==1):
                tk.Label(Container,text='ระยะทาง:', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            if(i==2):
                tk.Label(Container,text='เวลา:', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            if(i==3):
                tk.Label(Container,text='ค่าเดินทาง:', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)

        self.Containers.append(Container)
        self.inputxts.append(inputtxt)
        self.Containers[-1].pack(padx=5, pady=5,side=tk.TOP) 


        
 
        tmp = tk.Frame(self,bg=frame_bg,height="3",width="1600")
        tmp.pack(padx=20,pady=20,side=tk.TOP)
        tk.Button(tmp, text='เพิ่มเส้นทาง', font=(font, font_body_size),width=10, height=1,command=lambda: self.add(self.Con)).pack(padx=20, pady=20, side=tk.LEFT)
        tk.Button(tmp, text='ลบเส้นทาง', font=(font, font_body_size),width=10, height=1,command=lambda: self.remove(self.Con)).pack(padx=20, pady=20, side=tk.LEFT)

        self.errtxt=StringVar()
        self.errtxt.set("")
        self.err= tk.Label(self,textvariable=self.errtxt,font=(font,font_body_size),width=50, height=1,fg="red",bg=frame_bg)
        self.err.pack(padx=20,pady=20,side=tk.TOP)
        
        tk.Button(self, text='ย้อนกลับ', font=(font, font_body_size),width=20, height=1,command=lambda: master.switch_frame(StartPage)).pack(padx=400, pady=20, side=tk.LEFT)
        tk.Button(self, text='บันทึก', font=(font, font_body_size),width=20, height=1,command=lambda: self.save(master)).pack(padx=0, pady=20, side=tk.LEFT)

        
    def add(self,master):
        Container = tk.Frame(self.Con,bg=frame_bg,height="3",width="1600")
        inputtxt = [tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20),tk.Text(Container,height = 1,width = 20)]
        for i in range(5):
            if(i==0):
                tk.Label(Container,text='เส้นทางจาก', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            inputtxt[i].pack(padx=20,pady=20, side=tk.LEFT)
            if(i==0):
                tk.Label(Container,text=' --> ', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            if(i==1):
                tk.Label(Container,text='ระยะทาง:', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            if(i==2):
                tk.Label(Container,text='เวลา:', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)
            if(i==3):
                tk.Label(Container,text='ค่าเดินทาง:', font=(font,font_body_size), fg=font_col,bg=frame_bg).pack(side=tk.LEFT)

        self.Containers.append(Container)
        self.inputxts.append(inputtxt)
        self.Containers[-1].pack(padx=5, pady=5,side=tk.TOP)
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

    def remove(self,master):
        if(len(self.Containers)<=1):return
        self.Containers[-1].pack_forget()
        self.Containers.pop()
        self.inputxts.pop()
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
    
    def save(self,master):
        if self.startinp.get(1.0,"end-1c")=="":
            self.errtxt.set("โปรดใส่จุดเริ่มต้น")
            print("Null")
            return
        if self.inputxts[0][0].get(1.0,"end-1c")=="" or self.inputxts[0][1].get(1.0,"end-1c")=="" or self.inputxts[0][2].get(1.0,"end-1c")=="" or self.inputxts[0][3].get(1.0,"end-1c")=="" or self.inputxts[0][4].get(1.0,"end-1c")=="":
            self.errtxt.set("โปรดใส่เส้นทางอย่่างน้อย 1 เส้น")
            return
        exportcell={}
        exportcell[self.startinp.get(1.0,"end-1c")]=[self.startinp.get(1.0,"end-1c")]
        lis=[]
        lis.append(self.startinp.get(1.0,"end-1c"))
        mx=-1
        for i in range(len(self.Containers)):
            start=self.inputxts[i][0].get(1.0,"end-1c")
            end=self.inputxts[i][1].get(1.0,"end-1c")
            dis=self.inputxts[i][2].get(1.0,"end-1c")
            time=self.inputxts[i][3].get(1.0,"end-1c")
            cost=self.inputxts[i][4].get(1.0,"end-1c")
            if not self.isfloat(dis) or not self.isfloat(time) or not self.isfloat(cost):
                self.errtxt.set("โปรดใส่ ระยะทาง เวลา ค่าใช้จ่าย เป็นตัวเลข")
                return
            if not start in exportcell:
                lis.append(start)
                exportcell[start]=[]
                exportcell[start].append(start)
            if not end in exportcell:
                lis.append(end)
                exportcell[end]=[]
                exportcell[end].append(end)
            s=end+","+dis+","+time+","+cost
            exportcell[start].append(s)
            mx=max(len(exportcell[start]),len(exportcell[end]),mx)
        for key,val in exportcell.items():
            while len(exportcell[key])<mx:
                exportcell[key].append("")
        
        data_export=pd.DataFrame(exportcell,columns=lis)
        data_export=data_export.T
        data_export.to_excel(r'Input Data.xlsx',index=False,header=True)
        self.reset()

        master.switch_frame(StartPage)
    def reset(self):
        #========================================
        global l,allplace,chboxVar,exportdata,chbox
        exportdata=pd.read_excel('Export Data.xlsx')
        l=exportdata.values.tolist()
        allplace=l[-1][-3].split(',')
        chboxVar={}
        chbox=[0]
        #========================================
    def isfloat(self,num):
        try:
            float(num)
            return True
        except ValueError:
            return False
        

class ResultPage(tk.Frame):
    def __init__(self, master):
        
        tk.Frame.__init__(self,master,bg=frame_bg)
        tk.Label(self, text="เส้นทางที่ดีที่สุดและเส้นทางที่ใกล้เคียง", font=(font,font_header_size), fg=font_col,bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)
        dpearson,tpearson,cpearson,dcosine,tcosine,ccosine,covDis,covTime,covCost=calculate()
        pearson=[dpearson,tpearson,cpearson]
        cosine=[dcosine,tcosine,ccosine]

        tabControl = ttk.Notebook(self,width=1200, height=500)
        tab_ = [ttk.Frame(tabControl),ttk.Frame(tabControl),ttk.Frame(tabControl),ttk.Frame(tabControl)]
        tabControl_ = [ttk.Notebook(tab_[0],width=1150, height=500),ttk.Notebook(tab_[1],width=1150, height=500),ttk.Notebook(tab_[2],width=1150, height=500),ttk.Notebook(tab_[3],width=1150, height=500)]
        tab__= [[tk.Frame(tabControl_[0]),ttk.Frame(tabControl_[0]),ttk.Frame(tabControl_[0])],
               [ttk.Frame(tabControl_[1]),ttk.Frame(tabControl_[1]),ttk.Frame(tabControl_[1])],
               [ttk.Frame(tabControl_[2]),ttk.Frame(tabControl_[2]),ttk.Frame(tabControl_[2])],
               [ttk.Frame(tabControl_[3]),ttk.Frame(tabControl_[3]),ttk.Frame(tabControl_[3])]]

        tabControl.add(tab_[0], text='Pearson Similarity')
        tabControl.add(tab_[1], text='Cosine Similarity')
        tabControl.add(tab_[2], text='Covariance matrix')
        # tabControl.add(tab_[3], text='Graph')
        #==================================================================================================
        for i in range(2):
            tabControl_[i].add(tab__[i][0], text='เส้นทางที่ระยะทางสั้นที่สุด')
            tabControl_[i].add(tab__[i][1], text='เส้นทางที่ใช้เวลาน้อยที่สุด')
            tabControl_[i].add(tab__[i][2], text='เส้นทางที่ค่าใช้จ่ายน้อยที่สุด')
        for i in range(2,3):
            tabControl_[i].add(tab__[i][0], text='ข้อมูลของเส้นทางที่ระยะทางน้อยที่สุด')
            tabControl_[i].add(tab__[i][1], text='ข้อมูลของเส้นทางที่ใช้เวลาน้อยที่สุด')
            tabControl_[i].add(tab__[i][2], text='ข้อมูลของเส้นทางที่ค่าใช้จ่ายน้อยที่สุด')
        tabControl.pack(padx=0, pady=20, side=tk.TOP)
        tabControl_[0].pack(padx=0, pady=0, side=tk.TOP)
        tabControl_[1].pack(padx=0, pady=0, side=tk.TOP)
        tabControl_[2].pack(padx=0, pady=0, side=tk.TOP)
        tabControl_[3].pack(padx=0, pady=0, side=tk.TOP)
        #==================================================================================================
        ttk.Label(tab__[0][0],text='เส้นทางที่ระยะทางสั้นที่สุด(เรียงตามค่า Pearson จากมากไปน้อย)', font=(font,font_table_size)).grid(column=0,row=0,padx=10,pady=0)
        ttk.Label(tab__[0][1],text='เส้นทางที่ใช้เวลาเดินทางน้อยสุด(เรียงตามค่า Pearson จากมากไปน้อย)', font=(font,font_table_size)).grid(column=0,row=0,padx=10,pady=0)
        ttk.Label(tab__[0][2],text='เส้นทางที่ค่าใช้จ่ายน้อยที่สุด(เรียงตามค่า Pearson จากมากไปน้อย)', font=(font,font_table_size)).grid(column=0,row=0,padx=10,pady=0)
        for i in range(3):
            ttk.Label(tab__[0][i],text='ระยะทาง(km),เวลา(นาที),ราคา(บาท)', font=(font,font_table_size)).grid(column=1,row=0,padx=10,pady=0)
            ttk.Label(tab__[0][i],text='ค่า Peason Similarity', font=(font,font_table_size)).grid(column=2,row=0,padx=10,pady=0)
        prev=[0,0,0]
        tmp=0
        for i in range(5):
            for j in range(3):
                if not pearson[j].empty(): tmp=pearson[j].get()
                while(prev[j]!=0 and (l[tmp[1]][5]==l[prev[j][1]][5] or l[tmp[1]][6]==l[prev[j][1]][6] or prev[j][0]==tmp[0]) and not pearson[j].empty()):
                    tmp=pearson[j].get()
                s=l[tmp[1]][1]
                nnn=110
                while nnn<len(s):
                    s=s[:nnn]+"\n"+s[nnn:]
                    nnn+=110
                ttk.Label(tab__[0][j], text=s, font=(font,font_table_size)).grid(column=0,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[0][j], text=l[tmp[1]][5], font=(font,font_table_size)).grid(column=1,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[0][j], text=str(-tmp[0]), font=(font,font_table_size)).grid(column=2,row=i+1,padx=10,pady=0,sticky='W')
                prev[j]=tmp
        #==================================================================================================
        ttk.Label(tab__[1][0],text='เส้นทางที่ระยะทางสั้นที่สุด(เรียงตามค่า Cosine จากมากไปน้อย)', font=(font,font_table_size)).grid(column=0,row=0,padx=10,pady=0)
        ttk.Label(tab__[1][1],text='เส้นทางที่ใช้เวลาเดินทางน้อยสุด(เรียงตามค่า Cosine จากมากไปน้อย)', font=(font,font_table_size)).grid(column=0,row=0,padx=10,pady=0)
        ttk.Label(tab__[1][2],text='เส้นทางที่ค่าใช้จ่ายน้อยที่สุด(เรียงตามค่า Cosine จากมากไปน้อย)', font=(font,font_table_size)).grid(column=0,row=0,padx=10,pady=0)
        for i in range(3):
            ttk.Label(tab__[1][i],text='ระยะทาง(km),เวลา(นาที),ราคา(บาท)', font=(font,font_table_size)).grid(column=1,row=0,padx=10,pady=0)
            ttk.Label(tab__[1][i],text='ค่า Cosine Similarity', font=(font,font_table_size)).grid(column=2,row=0,padx=10,pady=0)
        prev=[0,0,0]
        tmp=0
        for i in range(0,5):
            for j in range(3):
                if not cosine[j].empty(): tmp=cosine[j].get()
                while(prev[j]!=0 and (l[tmp[1]][5]==l[prev[j][1]][5] or l[tmp[1]][6]==l[prev[j][1]][6] or prev[j][0]==tmp[0]) and not cosine[j].empty()):
                    tmp=cosine[j].get()
                s=l[tmp[1]][1]
                nnn=110
                while nnn<len(s):
                    s=s[:nnn]+"\n"+s[nnn:]
                    nnn+=110
                ttk.Label(tab__[1][j], text=s, font=(font,font_table_size)).grid(column=0,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[1][j], text=l[tmp[1]][5], font=(font,font_table_size)).grid(column=1,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[1][j], text=str(-tmp[0]), font=(font,font_table_size)).grid(column=2,row=i+1,padx=10,pady=0,sticky='W')
                prev[j]=tmp
        #==================================================================================================
        for i in range(3):
            ttk.Label(tab__[2][i],text='ระยะทาง',font=(font,font_table_size)).grid(column=1,row=0,padx=10,pady=0)
            ttk.Label(tab__[2][i],text='เวลา',font=(font,font_table_size)).grid(column=2,row=0,padx=10,pady=0)
            ttk.Label(tab__[2][i],text='ค่าใช้จ่าย',font=(font,font_table_size)).grid(column=3,row=0,padx=10,pady=0)
            ttk.Label(tab__[2][i],text='ระยะทาง',font=(font,font_table_size)).grid(column=0,row=1,padx=10,pady=0)
            ttk.Label(tab__[2][i],text='เวลา',font=(font,font_table_size)).grid(column=0,row=2,padx=10,pady=0)
            ttk.Label(tab__[2][i],text='ค่าใช้จ่าย',font=(font,font_table_size)).grid(column=0,row=3,padx=10,pady=0)
            for j in range(3):
                ttk.Label(tab__[2][0],text=str(covDis[i][j]),font=(font,font_table_size)).grid(column=i+1,row=j+1,padx=10,pady=0)
                ttk.Label(tab__[2][1],text=str(covTime[i][j]),font=(font,font_table_size)).grid(column=i+1,row=j+1,padx=10,pady=0)
                ttk.Label(tab__[2][2],text=str(covCost[i][j]),font=(font,font_table_size)).grid(column=i+1,row=j+1,padx=10,pady=0)
        #==================================================================================================
        
        #==================================================================================================
        tk.Button(self, text='เลือกสถานที่ใหม่', font=(font, font_body_size),width=20, height=1,command=lambda: master.switch_frame(StartPage)).pack(padx=20, pady=20, side=tk.TOP)

if __name__ == "__main__": #Just make sure this file can't be import by other file.
    app = SampleApp()
    app.title("TSP.exe")
    app.geometry('1600x900')
    app.resizable(width=False, height=False)
    app.configure(bg=bg)
    app.mainloop()

