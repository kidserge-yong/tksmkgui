import tkinter as tk
import tkgraphplot
import smkcontrol
import numpy as np

class smkgui(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.plotFrame = tk.Frame(self.master)
        self.plotFrame.grid(row = 0, column = 0, sticky="nsew")
        self.tkplot = tkgraphplot.tkEMGplot(self.plotFrame)

        self.controlFrame = tk.Frame(self.master)
        self.controlFrame.grid(row = 0, column = 2, sticky="nsew")
        self.tkcontrol = smkcontrol.tkEMGcontrol(self.controlFrame)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.plotFrame.rowconfigure(0, weight=1)
        self.plotFrame.columnconfigure(0, weight=1)

        self.controlFrame.rowconfigure(0, weight=1)
        self.controlFrame.columnconfigure(0, weight=1)

        self.quit = tk.Button(self.master, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row = 1, column = 2, pady=0)

        

        print("Finish create widgets")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = smkgui(master=root)
while True:
    if hasattr(app.tkcontrol, 'smk') and hasattr(app.tkplot, 'databuffer'):
        if app.tkcontrol.smk.is_new_data:
            app.tkplot.addDatapoint(np.array(app.tkcontrol.smk.emg()).reshape((1,32)))
            
    app.update_idletasks()
    app.update()