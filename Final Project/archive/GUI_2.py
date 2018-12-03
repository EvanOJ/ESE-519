import tkinter as tk 
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg") #matplotlib backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #change from "NavigationToolbar2TkAgg" to "NavigationToolbar2Tk"
from matplotlib.figure import Figure 
import matplotlib.animation as animation
from matplotlib import style
import os
import pygame


screenWidth = 480
screenHeight = 320

LARGE_FONT = ("Verdana",12)
style.use("ggplot")

global bufferLen
global freq
global startBuffer
global endBuffer
bufferLen = 600
startBuffer = 0 
freq = 120
endBuffer = 600

#figure data, constant 
f = Figure(figsize=(5,5),dpi=100)
ax1 = f.add_subplot(111)

def convertMATtoTXT(matfile):
    import scipy.io
    import pandas as pd
    mat = scipy.io.loadmat(matfile)
    #array = np.fromiter(mat.items(),dtype='int16',count=len(mat))
    ekg = mat['val'][0]
    out = pd.DataFrame(ekg)

    #out.to_csv("matOut.csv")
    ##out.to_csv("mat file.csv")
    return out

def pullData(path):
    pullData = open(path,"r").read()
    dataList = pullData.split('\n')
    # xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            # x,y = eachLine.split(',')
            y = eachLine.split(',')
            #print(int(y[0]))
            #xList.append(int(x))
            yList.append(float(y[0]))
    return yList

def feedback(interval,screen):

    data = pullData("C:/Users/EOJ/Desktop/data_stream.csv")
    print(data)

    pygame.display.flip()
    screen.fill((255,0,255))

def animate(interval):
    #to convert new mat files to csv run this 
    #ekg = convertMATtoTXT("C:/Users/EOJ/Downloads/a103l.mat")

    data = pullData("C:/Users/EOJ/Desktop/data_stream.csv")
    global bufferLen
    global startBuffer
    global endBuffer

    if len(data)>bufferLen:
        ax1.clear()
        print(startBuffer)
        print(endBuffer)
        ax1.plot(data[startBuffer:endBuffer])
        startBuffer += freq
        endBuffer += freq
    else:
        ax1.clear()
        ax1.plot(data)
        
    # pullData = open("C:/Users/EOJ/Desktop/data_stream.csv","r").read()
    # dataList = pullData.split('\n')
    # # xList = []
    # yList = []
    # for eachLine in dataList:
    #     if len(eachLine)>1:
    #         # x,y = eachLine.split(',')
    #         y = eachLine.split(',')
    #         print(int(y[0]))
    #         #xList.append(int(x))
    #         yList.append(int(y[0]))
    #ax1.clear() #clear the subplot to or it will continue to plot, eat up RAM
    #ax1.plot(yList)

class GUI(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self,"TEST GUI v1.0")
        container = tk.Frame(self)

        container.pack(side="top",fill="both",expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames = {}

        for Frame in (MainPage, graphPage,feedbackPage):

            frame = Frame(container,self)

            self.frames[Frame] = frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()



class MainPage(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Main Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self,text="Graph Page",
            command=lambda: controller.show_frame(graphPage))

        #add button to container, pack
        button1.pack()

        button3 = tk.Button(self,text="Feedback Page",
            command=lambda: controller.show_frame(feedbackPage))

        #add button to container, pack
        button3.pack()


class graphPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Graph Page",font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self,text="Go Back to Main Page",
            command=lambda: controller.show_frame(MainPage))

        #add button to container, pack
        button2.pack()

        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw() #change, from "show" to "draw"
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

class feedbackPage(tk.Frame):
    def __init__(self,parent,controller):

        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Feedback",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button4 = tk.Button(self,text="Go Back to Main Page",
            command=lambda: controller.show_frame(MainPage))

        #add button to container, pack
        button4.pack()

        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        screen = pygame.display.set_mode((screenWidth,screenHeight))
        # pygame.display.init()
        # screen = pygame.display.set_mode((screenWidth,screenHeight))
        # pygame.display.flip()
        # screen.fill((255,255,255))



app = GUI()

ani = animation.FuncAnimation(f,animate,interval=1500) #send to figure first then run the animate function at interval (ms) e.g. 1000ms = 1s

feedback = animation.FuncAnimation(f,feedback,interval=2000,screen=feedbackPage.screen)

app.mainloop()





