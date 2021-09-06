import tkinter as tk
import numpy as np
from serial.tools import list_ports
from smk import *

class tkEMGcontrol(tk.Frame):
    def __init__(self, master=None, channel_num=32, period=500):
        tk.Frame.__init__(self,master)
        self.master = master
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=0)
        self.master.rowconfigure(3, weight=1)

        self.is_serialconnect = False
        self.is_start = False
        
        self.createWidgets()

    def __del__(self):
        if hasattr(self, 'smk'):
            self.smk.stop()
            time.sleep(1.000)
            del self.smk
    
    def createWidgets(self):

        serialportlist = list_ports.comports()
        serialportlistname = {}
        for serialport in serialportlist:
            serialportlistname[str(serialport)[0:5]] = serialport
        
        serialportvariable = tk.StringVar(self.master)
        serialportvariable.set(list(serialportlistname.keys())[0])

        self.serialportselect = tk.OptionMenu(self.master, serialportvariable, *list(serialportlistname.keys()))
        self.serialportselect.grid(row = 0, column = 0, columnspan = 2, padx=5, pady=5, sticky="nsew")
        self.serialportselect.columnconfigure(0, weight=1)
        self.serialportselect.rowconfigure(0, weight=1)

        self.serialportconnect = tk.Button(self.master)
        self.serialportconnect["text"] = "Connect to serial port"
        self.serialportconnect["command"] = lambda: self.connectSMK(serialportlistname[serialportvariable.get()])
        self.serialportconnect.grid(row = 1, column = 0, columnspan = 2, padx=5, pady=5, sticky="nsew")
        self.serialportconnect.columnconfigure(1, weight=1)
        self.serialportconnect.rowconfigure(1, weight=1)

        self.radiobutton = []
        emgtypevariable = tk.StringVar(self.master, 'EMG')
        emgtype = [
            "EMG", "IEMG"
        ]
        for i, item in enumerate(emgtype):
            r = tk.Radiobutton(self.master, text = item, variable = emgtypevariable, 
                    value = item, indicator = 1, state = tk.DISABLED,
                    background = "light blue")
            r.grid(row = 2, column = i, ipadx=5, ipady=5, sticky="nsew")
            self.radiobutton.append(r)

        self.startstopbutton = tk.Button(self.master)
        self.startstopbutton["text"] = "Start"
        self.startstopbutton["command"] = lambda: self.startstopmanager(emgtypevariable.get())
        self.startstopbutton.grid(row = 3, column = 0, columnspan = 2, padx=5, pady=5, sticky="nsew")
        self.startstopbutton.columnconfigure(2, weight=1)
        self.startstopbutton.rowconfigure(2, weight=1)
        self.startstopbutton["state"] = tk.DISABLED

        # self.hi_there = tk.Button(self.master)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.grid(row = 5, column = 0, columnspan = 2, padx=5, pady=5, sticky="nsew")

    def connectSMK(self, serialport):
        if self.is_serialconnect == False:
            if type(serialport) is serial.tools.list_ports_common.ListPortInfo:
                self.smk = smk_arrayemg(serialport)
                self.serialportconnect["text"] = "Connected\n Click here to disconnect"
                self.serialportselect["state"] = tk.DISABLED
                for item in self.radiobutton:
                    item["state"] = tk.NORMAL
                self.startstopbutton["state"] = tk.NORMAL
                self.is_serialconnect = True
            else:
                self.serialportconnect["text"] = "Wrong Serial port\nConnect to serial port"
        else:
            self.smk.stop()
            time.sleep(1.000)
            del self.smk
            self.serialportconnect["text"] = "Connect to serial port"
            self.serialportselect["state"] = tk.NORMAL
            for item in self.radiobutton:
                item["state"] = tk.DISABLED
            self.startstopbutton["state"] = tk.DISABLED
            self.is_serialconnect = False


    def startstopmanager(self, emgtype):
        if not hasattr(self, 'smk'):
            self.startstopbutton["text"] = "Please connect to serial port first\n"

        if self.is_start:
            self.smk.stop()
            self.is_start = False
            self.startstopbutton["text"] = "Start"
        else:
            self.smk.calibrate()
            self.smk.start_lsl()
            self.smk.start(str(emgtype))
            self.is_start = True
            self.startstopbutton["text"] = "Stop"
    
        print(str(emgtype))




if __name__ == '__main__':
    root = tk.Tk()
    app = tkEMGcontrol(master=root)
    app.mainloop()
