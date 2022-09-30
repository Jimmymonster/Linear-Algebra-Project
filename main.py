import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import openpyxl
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
inputdata=pd.read_excel('Input Data.xlsx','Car')
l=inputdata.values.tolist()
key={}
node = len(l)
for i in range(node):
    key[l[i][0]]=i
    key[i]=l[i][0]
#============================================
exportdata=pd.read_excel('Export Data.xlsx')
l=exportdata.values.tolist()
allplace=l[-1][-1].split(',')
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
    for i in range(oneset):
        if(chvisited(i,visited[0])):
            d=[float(_) for _ in l[i][5].split(',')]
            dmean=sum(d)/3
            pqDpearson.put([-findPearson(dtar,mean[0],d,dmean),i])
            pqDcosine.put([-findCosine(dtar,d),i])
        if(chvisited(i+oneset,visited[1])):
            t=[float(_) for _ in l[i+oneset][5].split(',')]
            tmean=sum(t)/3
            pqTpearson.put([-findPearson(ttar,mean[1],t,tmean),i+oneset])
            pqTcosine.put([-findCosine(ttar,t),i+oneset])
        if(chvisited(i+oneset+oneset,visited[2])):
            c=[float(_) for _ in l[i+oneset+oneset][5].split(',')]
            cmean=sum(c)/3
            pqCpearson.put([-findPearson(ctar,mean[2],c,cmean),i+oneset+oneset])
            pqCcosine.put([-findCosine(ctar,c),i+oneset+oneset])
    return pqDpearson,pqTpearson,pqCpearson,pqDcosine,pqTcosine,pqCcosine

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
        tk.Frame.__init__(self,master,bg=frame_bg)
        tk.Label(self, text="เลือกสถานที่ที่คุณอยากจะไป เราจะเลือกเส้นทางที่ดีที่สุดให้คุณ", font=(font,font_header_size), fg=font_col,bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)
        tk.Label(self, text=allplace[0] + " จุดเริ่มต้น ",font={font,font_body_size}, fg=font_col,bg=frame_bg).pack(padx=0,pady=5,side=tk.TOP)
        for i in range(1,len(allplace)):
            chboxVar[allplace[i]]=tk.IntVar()
            chbox.append(tk.Checkbutton())
            chbox[i]=tk.Checkbutton(self,text=allplace[i],variable=chboxVar[allplace[i]],font={font,font_body_size},fg=font_col,bg=frame_bg,activebackground=frame_bg,activeforeground=font_col,selectcolor=frame_bg)
            chbox[i].pack(padx=0,pady=5,side=tk.TOP)
        
        tk.Button(self, text='เริ่มคำนวนเส้นทาง', font=(font, font_body_size),width=20, height=1,command=lambda: master.switch_frame(ResultPage) if(self.check()) else self.erro(master)).pack(padx=20, pady=20, side=tk.TOP)
    # check if every items is not select
    def check(self):
        ch=False
        for i in range(1,len(allplace)):
            if(chboxVar[allplace[i]].get()):
                ch=True
        return ch
    def erro(self,master):
        tk.Label(self, text="เลือกสักที่สิ", font=(font,font_header_size), fg="red",bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)

class ResultPage(tk.Frame):
    def __init__(self, master):
        
        tk.Frame.__init__(self,master,bg=frame_bg)
        tk.Label(self, text="เส้นทางที่ดีที่สุดและเส้นทางที่ใกล้เคียง", font=(font,font_header_size), fg=font_col,bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)
        dpearson,tpearson,cpearson,dcosine,tcosine,ccosine=calculate()
        pearson=[dpearson,tpearson,cpearson]
        cosine=[dcosine,tcosine,ccosine]

        tabControl = ttk.Notebook(self,width=1200, height=400)
        tab_ = [ttk.Frame(tabControl),ttk.Frame(tabControl)]
        tabControl_ = [ttk.Notebook(tab_[0],width=1150, height=350),ttk.Notebook(tab_[1],width=1150, height=350)]
        tab__= [[tk.Frame(tabControl_[0]),ttk.Frame(tabControl_[0]),ttk.Frame(tabControl_[0])],
               [ttk.Frame(tabControl_[1]),ttk.Frame(tabControl_[1]),ttk.Frame(tabControl_[1])]]

        tabControl.add(tab_[0], text='Pearson Similarity')
        tabControl.add(tab_[1], text='Cosine Similarity')
        for i in range(2):
            tabControl_[i].add(tab__[i][0], text='เส้นทางที่ระยะทางสั้นที่สุด')
            tabControl_[i].add(tab__[i][1], text='เส้นทางที่ใช้เวลาน้อยที่สุด')
            tabControl_[i].add(tab__[i][2], text='เส้นทางที่ค่าใช้จ่ายน้อยที่สุด')
        tabControl.pack(padx=0, pady=20, side=tk.TOP)
        tabControl_[0].pack(padx=0, pady=0, side=tk.TOP)
        tabControl_[1].pack(padx=0, pady=0, side=tk.TOP)
        
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
                s=s[:110]+"\n"+s[110:]
                ttk.Label(tab__[0][j], text=s, font=(font,font_table_size)).grid(column=0,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[0][j], text=l[tmp[1]][5], font=(font,font_table_size)).grid(column=1,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[0][j], text=str(-tmp[0]), font=(font,font_table_size)).grid(column=2,row=i+1,padx=10,pady=0,sticky='W')
                prev[j]=tmp

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
                s=s[:110]+"\n"+s[110:]
                ttk.Label(tab__[1][j], text=s, font=(font,font_table_size)).grid(column=0,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[1][j], text=l[tmp[1]][5], font=(font,font_table_size)).grid(column=1,row=i+1,padx=10,pady=0,sticky='W')
                ttk.Label(tab__[1][j], text=str(-tmp[0]), font=(font,font_table_size)).grid(column=2,row=i+1,padx=10,pady=0,sticky='W')
                prev[j]=tmp

        tk.Button(self, text='เลือกสถานที่ใหม่', font=(font, font_body_size),width=20, height=1,command=lambda: master.switch_frame(StartPage)).pack(padx=20, pady=20, side=tk.TOP)

if __name__ == "__main__": #Just make sure this file can't be import by other file.
    app = SampleApp()
    app.title("TSP.exe")
    app.geometry('1280x720')
    app.resizable(width=False, height=False)
    app.configure(bg=bg)
    app.mainloop()

