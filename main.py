import tkinter as tk
import pandas as pd
import numpy as np
import openpyxl 

# Global Var
bg='black'
frame_bg='black'

font='TH Sarabun New'
font_header_size=40
font_body_size=20
font_col='white'
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
        tk.Label(self, text="This is first Page", font=(font,font_header_size), fg=font_col,bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)
        tk.Button(self, text='Go to Next Page', font=(font, font_body_size),width=30, height=2,command=lambda: master.switch_frame(InputPage)).pack(padx=20, pady=20, side=tk.TOP)

class InputPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self,master,bg=frame_bg)
        tk.Label(self, text="เลือกสถานที่ที่คุณอยากจะไป เราจะเลือกเส้นทางที่ดีที่สุดให้คุณ", font=(font,font_header_size), fg=font_col,bg=frame_bg).pack(padx=0, pady=20, side=tk.TOP)

if __name__ == "__main__": #Just make sure this file can't be import by other file.
    app = SampleApp()
    app.title("TSP.exe")
    app.geometry('1280x720')
    app.resizable(width=False, height=False)
    app.configure(bg=bg)
    app.mainloop()

