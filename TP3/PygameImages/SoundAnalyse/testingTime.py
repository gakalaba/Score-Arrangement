
import random
from Tkinter import *
import Recordyourvoice as rvc
import thread
import outputRecorded as opr
import time


done = False

def init(data):
    data.allGo = False
    data.color = "white"
    data.time = 0
    data.blinks = 1
    data.clicks = 0
    data.instructions = False
    data.symb = None
    data.recColor = "white"

    data.rhythms = []

def mousePressed(event, data):
    pass

def redrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill=data.color)
    if data.instructions:
        c = "                                   Please sing clearly and loudly into the microphone \n\
                                                   Sing only on the syllable 'Bah'\n\
                                                      Sing at a speed of 80 bpm\n\
                                            When you are ready, press the space bar to begin\n\
                    **But record one full silent/empty measure before beginning**"
        canvas.create_text(data.width//2, data.height//2, text=c)
    if data.symb != None:
        canvas.create_text(data.width//2, data.height//2, text = data.symb, font = "Helvetica 80", fill="white")
    if rvc.recording:
        canvas.create_oval(data.width//2 - 50, data.height//2-50,data.width//2 + 50, data.height//2 + 50, fill=data.recColor)

def keyPressed(event, data):
    if event.keysym == "space":
        if data.clicks == 0:
            data.clicks += 1
            data.instructions = True
        elif data.clicks == 1:
            data.instructions = False
            data.clicks = 0
            data.allGo = True
            thread.start_new_thread( timerFired, (data,))
            # thread.start_new_thread(rvc.inputSound,())

def timerFired(data):
    # print(data.time)
    # data.time += 1
    # if data.time%4 == 0:
    #     data.color = "white"
    # elif data.time%4 == 1:
    #     data.color = "black"

    
    if data.allGo:
        data.time += 1
        if data.time%12 == 0:
            if data.blinks < 5:
                # thread.start_new_thread(opr.play,('output1.wav',))
                data.color = "black"
                if not data.blinks == 4:
                    data.symb = str(4 - data.blinks)
                else:
                    data.symb = "SING"
                data.blinks += 1
            else:
                data.allGo = False
                data.blinks = 1
                data.time = 0
                data.rhythms = []
                data.start = time.time()
                thread.start_new_thread(rvc.inputSound,())
            # data.color = "black"
            # data.symb = str(data.blinks)
            # data.blinks += 1
        elif data.time%12 == 1:
            data.symb = None
            data.color = "white"
    if rvc.recording:
        data.time += 1
        if data.time%12 == 0:
            data.recColor = "white"
        elif data.time%12 == 1:
            data.recColor = "red"
        try:
            data.rhythms.append(rvc.notesSung[-1])
        except: pass
    # print("data.rhythms!", data.rhythms)
    # print(len(data.rhythms))
    

####################################
# use the run function as-is
####################################

def run(width=800, height=700):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = (250/3) # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

# run()
