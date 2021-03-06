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
                              command=self.safe_destroy)
        self.quit.grid(row = 1, column = 2, pady=0)

        

        print("Finish create widgets")

    def safe_destroy(self):
        if hasattr(app.tkcontrol, 'smk'):
            app.tkcontrol.smk.exitloop()
        self.master.destroy()

    def say_hi(self):
        print("hi there, everyone!")

if __name__ == '__main__':
    root = tk.Tk()
    app = smkgui(master=root)

    def draw_frame():
        '''Draws a new frame every N milliseconds'''
        if hasattr(app.tkcontrol, 'smk') and hasattr(app.tkplot, 'databuffer'):
            if app.tkcontrol.smk.is_new_data:
                app.tkplot.addDatapoint(np.array(app.tkcontrol.smk.emg()).reshape((1,32)))
        root.after(1, draw_frame)

    root.after_idle(draw_frame)
    try:
        root.mainloop()
    except Exception:
        print("Exception in Logging.")