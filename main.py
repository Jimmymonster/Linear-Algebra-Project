import tkinter as tk
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
    print(mean)
    pqD=PriorityQueue() # [Pearson similarity value , index]
    pqT=PriorityQueue() # [Pearson similarity value , index]
    pqC=PriorityQueue() # [Pearson similarity value , index]
    for i in range(oneset):
        if(chvisited(i,visited[0])):
            d=[float(_) for _ in l[i][5].split(',')]
            dmean=sum(d)/3
            pqD.put([-findPearson(dtar,mean[0],d,dmean),i])
        if(chvisited(i,visited[1])):
            t=[float(_) for _ in l[i+oneset][5].split(',')]
            tmean=sum(t)/3
            pqT.put([-findPearson(ttar,mean[1],t,tmean),i])
        if(chvisited(i,visited[2])):
            c=[float(_) for _ in l[i+oneset+oneset][5].split(',')]
            cmean=sum(c)/3
            pqC.put([-findPearson(ctar,mean[2],c,cmean),i])
    return pqD,pqT,pqC

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
        tk.Label(self, text="เส้นทางที่ดีที่สุด 5 อันดับคือ", font=(font,font_header_size), fg=font_col,bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)
        d,t,c=calculate()
        for i in range(0,5):
            print(d.get(),end=' ')
            print(t.get(),end=' ')
            print(c.get())
        tk.Button(self, text='เลือกสถานที่ใหม่', font=(font, font_body_size),width=20, height=1,command=lambda: master.switch_frame(StartPage)).pack(padx=20, pady=20, side=tk.TOP)

if __name__ == "__main__": #Just make sure this file can't be import by other file.
    app = SampleApp()
    app.title("TSP.exe")
    app.geometry('1280x720')
    app.resizable(width=False, height=False)
    app.configure(bg=bg)
    app.mainloop()

