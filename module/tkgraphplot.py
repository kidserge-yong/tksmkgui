import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

class tkEMGplot(tk.Frame):
    def __init__(self, master=None, channel_num=32, period=100):
        tk.Frame.__init__(self,master)
        self.fig = None
        self.canvas = None
        self.toolbar = None
        self.channel_num = channel_num
        self.period = period
        self.databuffer = np.zeros((period,32))
        self.createWidgets()
    
    def createWidgets(self):
        self.fig = Figure(figsize=(5, 4))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)  # A tk.DrawingArea.
        self.canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.master, pack_toolbar=False)
        self.toolbar.update()

        self.canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        self.canvas.mpl_connect("key_press_event", key_press_handler)

        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        
        # self.toolbar.grid(row = 1, column = 0)
        # self.canvas.get_tk_widget().grid(row = 0, column = 0)

        
        self.testbutton = tk.Button(self.master)
        self.testbutton["text"] = "Add one data point"
        self.testbutton["command"] = self.testaddDatapoint
        self.testbutton.pack(side=tk.LEFT, fill=tk.X, expand=False)

        self.testplot()

    def testaddDatapoint(self):
        new_data = ((np.random.rand(self.channel_num)-0.5) * 2) * 2.5
        self.addDatapoint(new_data)


    def testplot(self):
        self.fig.clear()
        t = np.arange(0, self.period, 1)
        datas = []

        ## Generate data for testing
        for i in range(self.channel_num):
            data = 2 * np.sin(2 * np.pi * t)+np.random.uniform(0,1,self.period)
            datas.append(data)
            # ax.spines['top'].set_visible(False)
            # ax.spines['right'].set_visible(False)
            # #ax.spines['bottom'].set_visible(False)
            # #ax.spines['left'].set_visible(False)
        
        self.graphplot(t, np.array(datas).T)


    def graphplot(self, t, datas):
        max_d, min_d = max(map(max,datas)), min(map(min,datas))
        range_d = round(abs(max_d) + abs(min_d))
        ax = self.fig.add_subplot(1,1,1)
        for i in range(self.channel_num):
            ax.plot(t, datas[:,i]+(range_d*i), label = ["Channel:" + str(i+1)])        ## potential future problem.
        
        self.fig.axes[0].set_yticks(np.arange(0, self.channel_num*range_d, range_d))

        labels = [0]*self.channel_num
        for i in range(self.channel_num):
            labels[i] = "Channel:" + str(i+1)
        self.fig.axes[0].set_yticklabels(labels)

        self.canvas.draw()

    def addDatapoint(self, new_datas):
        newlen = 1
        if newlen <= 0:
            return

        self.fig.clear(True) 
        self.databuffer[0:self.period - newlen,:] = self.databuffer[newlen:,:]
        self.databuffer[self.period - newlen:,:] = new_datas

        fz = 250
        t = np.arange(0, self.period/fz, 1/fz)
        self.graphplot(t, self.databuffer)

        

if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title("Embedding in Tk")

    plot = tkEMGplot(root)

    # fig = Figure(figsize=(5, 4), dpi=100)
    # t = np.arange(0, 3, .01)
    # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    # canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    # canvas.draw()

    # # pack_toolbar=False will make it easier to use a layout manager later on.
    # toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    # toolbar.update()


    # canvas.mpl_connect(
    #     "key_press_event", lambda event: print(f"you pressed {event.key}"))
    # canvas.mpl_connect("key_press_event", key_press_handler)

    button = tk.Button(master=root, text="Quit", command=root.quit)

    # Packing order is important. Widgets are processed sequentially and if there
    # is no space left, because the window is too small, they are not displayed.
    # The canvas is rather flexible in its size, so we pack it last which makes
    # sure the UI controls are displayed as long as possible.
    # button.grid(row = 0, column = 1)
    button.pack(side=tk.BOTTOM)
    # toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    tk.mainloop()