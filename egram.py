import tkinter as tk
from tkinter import *
from matplotlib.figure import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from serialComm import receiveParametersFromPacemaker
import datetime


# to add a new line of data for the egram graph from the pacemaker to a text file 
def getEgramData(newEgram, chosenCommPort):
    # check if this is a new Egram to overwrite the previous data in the text file
    if (not newEgram):
        dataFile = open("egramData.txt", "w")
    else:
        dataFile = open("egramData.txt", "a")

    # getting the current time to be used for the x axis values in the egram
    currentTime = datetime.datetime.now()

    str_year = str(currentTime.year)
    str_month = str(currentTime.month)
    str_day = str(currentTime.day)
    str_hour = str(currentTime.hour)
    str_minute = str(currentTime.minute)
    str_second = str(currentTime.second)
    str_microsecond = str(currentTime.microsecond)

    # read data from the pacemaker. The last two values in the list returned are the egram y values
    receiveData = receiveParametersFromPacemaker(chosenCommPort)[-2:]

    str_atrialData = str(round(receiveData[0],2))
    str_ventData = str(round(receiveData[1],2))

    # write a new line to the file of the datetime and the two values to be plotted
    dataFile.write(str_year + "," + str_month + "," + str_day + "," + str_hour + "," + str_minute + "," + str_second + "," + str_microsecond + "," + str_atrialData + "," + str_ventData + "\n")
    
    dataFile.close()



def plotEgram(egramCanvas, chosenCommPort):
    style.use('ggplot')
    figure = plt.figure(figsize = (13,8), dpi = 100)
    egramPlot = figure.add_subplot(1,1,1)
    egramSpecialCanvas = FigureCanvasTkAgg(figure, master = egramCanvas) 

    def animate(i):
        # write new data to the file
        getEgramData(i, chosenCommPort)

        # open the file and read the latest line
        readData = open('egramData.txt', 'r').read()
        dataArray = readData.split('\n')
        xs = []
        atrialV = []
        ventV = []
        #xticks = []

        for line in dataArray:
            if len(line) > 1:
                split = line.split(',')

                # the first 7 numbers are formatted into a date before they are added to the x values array
                xs.append(datetime.datetime(int(split[0]), int(split[1]), int(split[2]), int(split[3]), int(split[4]), int(split[5]), int(split[6])))
                atrialV.append(float(split[7]))
                ventV.append(float(split[8]))
                #xticks.append(str(split[3])+":"+str(split[4]) + ":" + str(split[5]) + ":" + str(split[6]))

        egramPlot.clear()

        # only want to plot the last 100 values
        xs = xs[-100:] 
        #xticks = xticks[-100:]
        atrialV = atrialV[-100:]
        ventV = ventV[-100:]

        # plot the atrial and ventricle data against time
        egramPlot.plot(xs,atrialV)
        egramPlot.plot(xs,ventV)

        egramPlot.set_title("Electrogram", fontsize = 18)
        egramPlot.set_xlabel('Time', fontsize=15)
        egramPlot.legend(["Atrium","Ventricle"])
        egramPlot.set_xlim(left=xs[0])
        egramPlot.set_ylim(bottom=0, top=1)
        egramPlot.set_ylabel('Signal (mV)', fontsize=15)

    figure.patch.set_facecolor('#B5C4D2')

    ani = animation.FuncAnimation(figure, animate, interval=10)
    
    egramSpecialCanvas.draw()
    egramSpecialCanvas.get_tk_widget().pack()