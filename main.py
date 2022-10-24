import tkinter as tk
from tkinter import *
from init import *
from egram import *
from serialComm import *
import serial
import serial.tools.list_ports
from matplotlib.figure import *
import matplotlib.pyplot as plt


# making main window
window = tk.Tk()
window.wm_title("Digital Controller Monitor")
window.geometry("1250x625")
window.resizable(False, False)

# global variables
width = 1250
height = 625
logo = PhotoImage(file="logo.gif")
smallerLogo = PhotoImage(file="smallerLogo.gif")
username = tk.StringVar()
password = tk.StringVar()
currentUserParamObject = create_new_user_para()
parameterNames = ["LRL", "URL", "maxSensorRate", "fixedAVDelay", "dynamicAVDelay", "sensedAVDelayOffset", "atrialAmp",
                 "ventAmp", "atrialWidth", "ventWidth", "atrialSensit", "ventSensit", "VRP", "ARP", "PVARP", "PVARPext",
                 "hysteresis", "rateSmoothing", "ATRDuration", "ATRFallbackMode", "ATRFallbackTime", "activityThreshold",
                 "reactionTime", "responseFactor", "recoveryTime"]
parameterStringList = "[LRL.get(), URL.get(), maxSensorRate.get(), fixedAVDelay.get(), dynamicAVDelay.get(), sensedAVDelayOffset.get(), atrialAmp.get(), ventAmp.get(), atrialWidth.get(), ventWidth.get(), atrialSensit.get(), ventSensit.get(), VRP.get(), ARP.get(), PVARP.get(), PVARPext.get(), hysteresis.get(), rateSmoothing.get(), ATRDuration.get(), ATRFallbackMode.get(), ATRFallbackTime.get(), activityThreshold.get(), reactionTime.get(), responseFactor.get(), recoveryTime.get()]"
chosenPort = StringVar(window)
chosenPort.set("---")

# used to return to sign in page/welcome page
def toWelcome(frame):
    global username
    global password
    username.set("")
    password.set("")
    frame.destroy()
    welcome()

# checks if a parameter field is disabled
def disabledField(mode, parameterName):
    value = eval("currentUserParamObject." + mode + "." + parameterName)
    return value == None

# resets/undoes changes to parameters on mode pages by reseting their values to whatever is currently saved in the file
def resetVals(LRL, URL, maxSensorRate, fixedAVDelay, dynamicAVDelay, sensedAVDelayOffset, atrialAmp, ventAmp, atrialWidth, ventWidth, atrialSensit, ventSensit, VRP, ARP, PVARP, PVARPext, hysteresis, rateSmoothing, ATRDuration, ATRFallbackMode, ATRFallbackTime, activityThreshold, reactionTime, responseFactor, recoveryTime, currentMode):
    global currentUserParamObject
    receivedParameters = [LRL, URL, maxSensorRate, fixedAVDelay, dynamicAVDelay, sensedAVDelayOffset, atrialAmp, ventAmp, atrialWidth, ventWidth, atrialSensit, ventSensit, VRP, ARP, PVARP, PVARPext, hysteresis, rateSmoothing, ATRDuration, ATRFallbackMode, ATRFallbackTime, activityThreshold, reactionTime, responseFactor, recoveryTime]
    for i in range(25):
        if (i == 21):
            # special case for activity threshold. Calls a getter which converts the number into the corresponding word.
            receivedParameters[i].set(eval("currentUserParamObject."+currentMode+".get_activityThreshold()"))
        elif (type(receivedParameters[i]) == Entry):
            # if its a entry field
            if (not disabledField(currentMode, parameterNames[i])):
                receivedParameters[i].delete(0,END)
                receivedParameters[i].insert(0,eval("currentUserParamObject."+currentMode+"."+parameterNames[i]))
        else:
            # if its a dropdown
            if (not disabledField(currentMode, parameterNames[i])): 
                if (eval("currentUserParamObject."+currentMode+"."+parameterNames[i]) == 0):
                    receivedParameters[i].set("Off")
                elif (eval("currentUserParamObject."+currentMode+"."+parameterNames[i]) == 1):
                    receivedParameters[i].set("On")
                else:
                    receivedParameters[i].set(eval("currentUserParamObject."+currentMode+"."+parameterNames[i]))     
            else:
                # disabled drop down field
                receivedParameters[i].set("")

# applies values entered into input boxes to the global object variable and saves them to the file too after checking they are valid
def applyVals(LRL, URL, maxSensorRate, fixedAVDelay, dynamicAVDelay, sensedAVDelayOffset, atrialAmp, ventAmp, atrialWidth, ventWidth, atrialSensit, ventSensit, VRP, ARP, PVARP, PVARPext, hysteresis, rateSmoothing, ATRDuration, ATRFallbackMode, ATRFallbackTime, activityThreshold, reactionTime, responseFactor, recoveryTime, currentMode, userNumber):
    global currentUserParamObject
    eval("currentUserParamObject.set_"+currentMode+"("+parameterStringList+")") # save to object variable
    save_user_para(userNumber, currentUserParamObject) # save to user's text file
    resetVals(LRL, URL, maxSensorRate, fixedAVDelay, dynamicAVDelay, sensedAVDelayOffset, atrialAmp, ventAmp, atrialWidth, ventWidth, atrialSensit, ventSensit, VRP, ARP, PVARP, PVARPext, hysteresis, rateSmoothing, ATRDuration, ATRFallbackMode, ATRFallbackTime, activityThreshold, reactionTime, responseFactor, recoveryTime, currentMode)
    
    # if apply is clicked on the mode that the pacemaker is currently operating on
    if (currentUserParamObject.get_sendMode() == currentMode):
        try:
            sendParametersToPacemaker(chosenPort.get(),eval("currentUserParamObject."+currentMode+".LRL"), eval("currentUserParamObject."+currentMode+".atrialAmp"), eval("currentUserParamObject."+currentMode+".ventAmp"), eval("currentUserParamObject."+currentMode+".atrialWidth"), eval("currentUserParamObject."+currentMode+".ventWidth"), eval("currentUserParamObject."+currentMode+".ARP"), eval("currentUserParamObject."+currentMode+".VRP"), eval("currentUserParamObject."+currentMode+".reactionTime"), eval("currentUserParamObject."+currentMode+".recoveryTime"), eval("currentUserParamObject."+currentMode+".maxSensorRate"), eval("currentUserParamObject."+currentMode+".responseFactor"), eval("currentUserParamObject."+currentMode+".fixedAVDelay"), eval("currentUserParamObject."+currentMode+".activityThreshold"), currentUserParamObject.sendMode)
            messagebox.showinfo(message="Applied parameters of "+currentMode+" sent to pacemaker.")
        except:
            checkPort = serial.Serial()
            checkPort.port = chosenPort.get()
            try:
                checkPort.open()
                checkPort.close()
            except:
                messagebox.showinfo(message="Pacemaker is no longer connected at this port.")

# verifies the username and password, and grants user access to log in accordingly 
def homepage(user, pswd, frame):

    # displays home screen
    def drawHomeScreen(frame):

        # general function to draw any of the 12 mode screens
        def drawModeScreen(frame, mode, title):
            frame.destroy()
            
            modeFrame = tk.Frame(window, bg="white")
            modeFrame.pack()

            # making canvas on the new mode frame
            newCanvas = Canvas(modeFrame, width=width, height=height)
            newCanvas.pack()
            newCanvas.configure(background='#B5C4D2')
            newCanvas.create_rectangle(40, 80, width-40, height-95, outline = "", fill = "#FFFFFF")

            newCanvas.create_text(625, 40, text = title, font=("Roboto", 28, "bold"), fill='black')

            headerFont = ["Roboto", 14, "bold"]
            unitFont = ["Roboto", 11, "bold"]

            # row 1
            newCanvas.create_text(55, 105, text = "Lower Rate Limit:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "LRL") else "black")
            newCanvas.create_rectangle(55, 135, 205, 165, outline="grey" if disabledField(mode, "LRL") else "black")
            entry_LRL = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "LRL") else "normal")
            entry_LRL.place(x = 56, y = 136, width = 149, height = 29)
            newCanvas.create_text(215, 140, text = "ppm", anchor = NW, font=(unitFont), fill="grey" if disabledField(mode, "LRL") else "black")

            newCanvas.create_text(293, 105, text = "Upper Rate Limit:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "URL") else "black")
            newCanvas.create_rectangle(293, 135, 443, 165, outline="grey" if disabledField(mode, "URL") else "black")
            entry_URL = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "URL") else "normal")
            entry_URL.place(x = 294, y = 136, width = 149, height = 29)
            newCanvas.create_text(453, 140, text = "ppm", anchor = NW, font=(unitFont), fill="grey" if disabledField(mode, "URL") else "black")

            newCanvas.create_text(530, 105, text = "Maximum Sensor \nRate:", anchor = W, font=(headerFont), fill="grey" if disabledField(mode, "maxSensorRate") else "black")
            newCanvas.create_rectangle(530, 135, 680, 165, outline="grey" if disabledField(mode, "maxSensorRate") else "black")
            entry_maxSensorRate = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "maxSensorRate") else "normal")
            entry_maxSensorRate.place(x = 531, y = 136, width = 149, height = 29)
            newCanvas.create_text(690, 140, text = "ppm", anchor = NW, font=(unitFont), fill="grey" if disabledField(mode, "maxSensorRate") else "black")

            newCanvas.create_text(767, 105, text = "Fixed AV Delay:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "fixedAVDelay") else "black")
            newCanvas.create_rectangle(767, 135, 917, 165, outline="grey" if disabledField(mode, "fixedAVDelay") else "black")
            entry_fixedAVDelay = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "fixedAVDelay") else "normal")
            entry_fixedAVDelay.place(x = 768, y = 136, width = 149, height = 29)
            newCanvas.create_text(927, 140, text = "ms", anchor = NW, font=(unitFont), fill="grey" if disabledField(mode, "fixedAVDelay") else "black")
                        
            newCanvas.create_text(1005, 106, text = "Dynamic AV Delay:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "dynamicAVDelay") else "black")
            var_dynamicAVDelay = StringVar(newCanvas)
            dropdown_dynamicAVDelay = OptionMenu(newCanvas, var_dynamicAVDelay, "Off", "On")
            dropdown_dynamicAVDelay.config(bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, bg= "#F5F5F5" if disabledField(mode, "dynamicAVDelay") else "white", borderwidth = 2, fg = 'black', relief=FLAT, state= "disabled" if disabledField(mode, "dynamicAVDelay") else "normal")
            dropdown_dynamicAVDelay.place(x = 1004, y = 135, width = 150, height = 30)
            newCanvas.create_rectangle(1003, 134, 1154, 165, outline="grey" if disabledField(mode, "dynamicAVDelay") else "black")
            newCanvas.create_text(1164, 140, text = "ms", anchor = NW, font=(unitFont), fill="grey" if disabledField(mode, "dynamicAVDelay") else "black")

            # row 2
            newCanvas.create_text(55, 190, text = "Sensed \nAV Delay Offset:", anchor = W, font=(headerFont), fill="grey" if disabledField(mode, "sensedAVDelayOffset") else "black")
            var_sensedAVDelayOffset = StringVar(newCanvas)
            dropdown_sensedAVDelayOffset = OptionMenu(newCanvas, var_sensedAVDelayOffset, "Off", "-10", "-20", "-30", "-40", "-50", "-60", "-70", "-80", "-90", "-100")
            dropdown_sensedAVDelayOffset.config(bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, bg= "#F5F5F5" if disabledField(mode, "sensedAVDelayOffset") else "white", borderwidth = 2, fg = 'black', relief=FLAT, state= "disabled" if disabledField(mode, "sensedAVDelayOffset") else "normal")
            dropdown_sensedAVDelayOffset.place(x = 56, y = 221, width = 149, height = 29)
            newCanvas.create_text(215, 235, text = "ms", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "sensedAVDelayOffset") else "black")
            newCanvas.create_rectangle(54, 219, 205, 250, outline="grey" if disabledField(mode, "sensedAVDelayOffset") else "black")

            newCanvas.create_text(293, 190, text = "Atrial Amplitude*:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "atrialAmp") else "black")
            newCanvas.create_rectangle(293, 220, 443, 250, outline="grey" if disabledField(mode, "atrialAmp") else "black")
            entry_atrialAmp = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "atrialAmp") else "normal")
            entry_atrialAmp.place(x = 294, y = 221, width = 149, height = 29)
            newCanvas.create_text(453, 235, text = "V", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "atrialAmp") else "black")

            newCanvas.create_text(530, 190, text = "Ventricular\nAmplitude*:", anchor = W, font=(headerFont), fill="grey" if disabledField(mode, "ventAmp") else "black")
            newCanvas.create_rectangle(530, 220, 680, 250, outline="grey" if disabledField(mode, "ventAmp") else "black")
            entry_ventAmp = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "ventAmp") else "normal")
            entry_ventAmp.place(x = 531, y = 221, width = 149, height = 29)
            newCanvas.create_text(690, 235, text = "V", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "ventAmp") else "black")

            newCanvas.create_text(767, 190, text = "Atrial Pulse Width:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "atrialWidth") else "black")
            newCanvas.create_rectangle(767, 220, 917, 250, outline="grey" if disabledField(mode, "atrialWidth") else "black")
            entry_atrialWidth = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "atrialWidth") else "normal")
            entry_atrialWidth.place(x = 768, y = 221, width = 149, height = 29)
            newCanvas.create_text(927, 235, text = "ms", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "atrialWidth") else "black")
            
            newCanvas.create_text(1004, 190, text = "Ventricular\nPulse Width:", anchor = W, font=(headerFont), fill="grey" if disabledField(mode, "ventWidth") else "black")
            newCanvas.create_rectangle(1004, 220, 1154, 250, outline="grey" if disabledField(mode, "ventWidth") else "black")
            entry_ventWidth = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "ventWidth") else "normal")
            entry_ventWidth.place(x = 1005, y = 221, width = 149, height = 29)
            newCanvas.create_text(1164, 235, text = "ms", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "ventWidth") else "black")

            # row 3
            newCanvas.create_text(55, 275, text = "Atrial Sensitivity:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "atrialSensit") else "black")
            newCanvas.create_rectangle(55, 305, 205, 335, outline="grey" if disabledField(mode, "atrialSensit") else "black")
            entry_atrialSensit = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "atrialSensit") else "normal")
            entry_atrialSensit.place(x = 56, y = 306, width = 149, height = 29)
            newCanvas.create_text(215, 320, text = "mV", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "atrialSensit") else "black")
            
            newCanvas.create_text(293, 275, text = "Ventricular\nSensitivity:", anchor = W, font=(headerFont), fill="grey" if disabledField(mode, "ventSensit") else "black")
            newCanvas.create_rectangle(293, 305, 443, 335, outline="grey" if disabledField(mode, "ventSensit") else "black")
            entry_ventSensit = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "ventSensit") else "normal")
            entry_ventSensit.place(x = 294, y = 306, width = 149, height = 29)
            newCanvas.create_text(453, 320, text = "mV", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "ventSensit") else "black")

            newCanvas.create_text(530, 275, text = "VRP:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "VRP") else "black")
            newCanvas.create_rectangle(530, 305, 680, 335, outline="grey" if disabledField(mode, "VRP") else "black")
            entry_VRP = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "VRP") else "normal")
            entry_VRP.place(x = 531, y = 306, width = 149, height = 29)
            newCanvas.create_text(690, 320, text = "ms", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "VRP") else "black")

            newCanvas.create_text(767, 275, text = "ARP:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "ARP") else "black")
            newCanvas.create_rectangle(767, 305, 917, 335, outline="grey" if disabledField(mode, "ARP") else "black")
            entry_ARP = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "ARP") else "normal")
            entry_ARP.place(x = 768, y = 306, width = 149, height = 29)
            newCanvas.create_text(927, 320, text = "ms", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "ARP") else "black")
            
            newCanvas.create_text(1004, 275, text = "PVARP:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "PVARP") else "black")
            newCanvas.create_rectangle(1004, 305, 1154, 335, outline="grey" if disabledField(mode, "PVARP") else "black")
            entry_PVARP = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "PVARP") else "normal")
            entry_PVARP.place(x = 1005, y = 306, width = 149, height = 29)
            newCanvas.create_text(1164, 320, text = "ms", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "PVARP") else "black")

            # row 4
            newCanvas.create_text(55, 360, text = "PVARP Extension:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "PVARPext") else "black")
            var_PVARPext = StringVar(newCanvas)
            dropdown_PVARPext = OptionMenu(newCanvas, var_PVARPext, "Off", "50", "100", "150", "200", "250", "300", "350", "400")
            dropdown_PVARPext.config(bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, bg= "#F5F5F5" if disabledField(mode, "PVARPext") else "white", borderwidth = 2, fg = 'black', relief=FLAT, state= "disabled" if disabledField(mode, "PVARPext") else "normal")
            dropdown_PVARPext.place(x = 56, y = 391, width = 149, height = 29)
            newCanvas.create_text(215, 405, text = "ms", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "PVARPext") else "black")
            newCanvas.create_rectangle(55, 390, 205, 420, outline="grey" if disabledField(mode, "PVARPext") else "black")

            newCanvas.create_text(293, 360, text = "Hysteresis*:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "hysteresis") else "black")
            newCanvas.create_rectangle(293, 390, 443, 420, outline="grey" if disabledField(mode, "hysteresis") else "black")
            entry_hysteresis = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "hysteresis") else "normal")
            entry_hysteresis.place(x = 294, y = 391, width = 149, height = 29)
            newCanvas.create_text(453, 405, text = "ppm", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "hysteresis") else "black")

            newCanvas.create_text(530, 360, text = "Rate Smoothing:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "rateSmoothing") else "black")
            var_rateSmoothing = StringVar(newCanvas)
            dropdown_rateSmoothing = OptionMenu(newCanvas, var_rateSmoothing, "Off", "3", "6", "9", "12", "15", "18", "21", "25")
            dropdown_rateSmoothing.config(bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, bg= "#F5F5F5" if disabledField(mode, "rateSmoothing") else "white", borderwidth = 2, fg = 'black', relief=FLAT, state= "disabled" if disabledField(mode, "rateSmoothing") else "normal")
            dropdown_rateSmoothing.place(x = 531, y = 391, width = 149, height = 29)
            newCanvas.create_text(690, 405, text = "%", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "rateSmoothing") else "black")
            newCanvas.create_rectangle(530, 390, 680, 420, outline="grey" if disabledField(mode, "rateSmoothing") else "black")

            newCanvas.create_text(767, 360, text = "ATR Duration:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "ATRDuration") else "black")
            newCanvas.create_rectangle(767, 390, 917, 420, outline="grey" if disabledField(mode, "ATRDuration") else "black")
            entry_ATRDuration = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "ATRDuration") else "normal")
            entry_ATRDuration.place(x = 768, y = 391, width = 149, height = 29)
            newCanvas.create_text(927, 405, text = "cc", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "ATRDuration") else "black")
            
            newCanvas.create_text(1004, 360, text = "ATR Fallback Mode:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "ATRFallbackMode") else "black")
            var_ATRFallbackMode = StringVar(newCanvas)
            dropdown_ATRFallbackMode = OptionMenu(newCanvas, var_ATRFallbackMode, "Off", "On")
            dropdown_ATRFallbackMode.config(bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, bg= "#F5F5F5" if disabledField(mode, "ATRFallbackMode") else "white", borderwidth = 2, fg = 'black', relief=FLAT, state= "disabled" if disabledField(mode, "ATRFallbackMode") else "normal")
            dropdown_ATRFallbackMode.place(x = 1005, y = 391, width = 149, height = 29)
            newCanvas.create_text(1164, 140, text = "ms", anchor = NW, font=(unitFont), fill="grey" if disabledField(mode, "ATRFallbackMode") else "black")
            newCanvas.create_rectangle(1004, 390, 1154, 420, outline="grey" if disabledField(mode, "ATRFallbackMode") else "black")

            # row 5
            newCanvas.create_text(55, 445, text = "ATR Fallback Time:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "ATRFallbackTime") else "black")
            newCanvas.create_rectangle(55, 475, 205, 505, outline="grey" if disabledField(mode, "ATRFallbackTime") else "black")
            entry_ATRFallbackTime = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "ATRFallbackTime") else "normal")
            entry_ATRFallbackTime.place(x = 56, y = 476, width = 149, height = 29)
            newCanvas.create_text(215, 490, text = "min", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "ATRFallbackTime") else "black")

            newCanvas.create_text(293, 445, text = "Activity Threshold:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "activityThreshold") else "black")
            var_activityThreshold = StringVar(newCanvas)
            dropdown_activityThreshold = OptionMenu(newCanvas, var_activityThreshold, "V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High")
            dropdown_activityThreshold.config(bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, bg= "#F5F5F5" if disabledField(mode, "activityThreshold") else "white", borderwidth = 2, fg = 'black', relief=FLAT, state= "disabled" if disabledField(mode, "activityThreshold") else "normal")
            dropdown_activityThreshold.place(x = 294, y = 476, width = 149, height = 29)
            newCanvas.create_text(1164, 140, text = "ms", anchor = NW, font=(unitFont), fill="grey" if disabledField(mode, "activityThreshold") else "black")
            newCanvas.create_rectangle(293, 475, 443, 505, outline="grey" if disabledField(mode, "activityThreshold") else "black")

            newCanvas.create_text(530, 445, text = "Reaction Time:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "reactionTime") else "black")
            newCanvas.create_rectangle(530, 475, 680, 505, outline="grey" if disabledField(mode, "reactionTime") else "black")
            entry_reactionTime = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "reactionTime") else "normal")
            entry_reactionTime.place(x = 531, y = 476, width = 149, height = 29)
            newCanvas.create_text(690, 490, text = "s", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "reactionTime") else "black")

            newCanvas.create_text(767, 445, text = "Response Factor:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "responseFactor") else "black")
            newCanvas.create_rectangle(767, 475, 917, 505, outline="grey" if disabledField(mode, "responseFactor") else "black")
            entry_responseFactor = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "responseFactor") else "normal")
            entry_responseFactor.place(x = 768, y = 476, width = 149, height = 29)
            
            newCanvas.create_text(1004, 445, text = "Recovery Time:", anchor = NW, font=(headerFont), fill="grey" if disabledField(mode, "recoveryTime") else "black")
            newCanvas.create_rectangle(1004, 475, 1154, 505, outline="grey" if disabledField(mode, "recoveryTime") else "black")
            entry_recoveryTime = Entry(newCanvas, bd = 3, font = ("Roboto", 14), highlightcolor = 'BLUE', highlightthickness = 1, relief = FLAT, state= "disabled" if disabledField(mode, "recoveryTime") else "normal")
            entry_recoveryTime.place(x = 1005, y = 476, width = 149, height = 29)
            newCanvas.create_text(1164, 490, text = "min", anchor = W, font=(unitFont), fill="grey" if disabledField(mode, "recoveryTime") else "black")
        
            newCanvas.create_text(40, height-85, text = "*Enter 0 for \"Off\"", anchor = NW, font=["Roboto", 12], fill="black")

            # calls resetVals to fill in values from user object's data
            resetVals(entry_LRL, entry_URL, entry_maxSensorRate, entry_fixedAVDelay, 
                var_dynamicAVDelay, var_sensedAVDelayOffset, entry_atrialAmp, entry_ventAmp, entry_atrialWidth, entry_ventWidth, 
                entry_atrialSensit, entry_ventSensit, entry_VRP, entry_ARP, entry_PVARP, var_PVARPext, 
                entry_hysteresis, var_rateSmoothing, entry_ATRDuration, var_ATRFallbackMode, entry_ATRFallbackTime, var_activityThreshold, 
                entry_reactionTime, entry_responseFactor, entry_recoveryTime, mode)

            # reset button
            resetButton = Button(newCanvas, text = "Undo", bg = '#777272', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', command=lambda: resetVals(entry_LRL, entry_URL, entry_maxSensorRate, entry_fixedAVDelay, 
                var_dynamicAVDelay, var_sensedAVDelayOffset, entry_atrialAmp, entry_ventAmp, entry_atrialWidth, entry_ventWidth, 
                entry_atrialSensit, entry_ventSensit, entry_VRP, entry_ARP, entry_PVARP, var_PVARPext, 
                entry_hysteresis, var_rateSmoothing, entry_ATRDuration, var_ATRFallbackMode, entry_ATRFallbackTime, var_activityThreshold, 
                entry_reactionTime, entry_responseFactor, entry_recoveryTime, mode))
            resetButton.place(x=500,y=560, width = 110, height = 30)

            # apply button
            applyButton = Button(newCanvas, text = "Apply", bg = '#D44949', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', command =lambda: applyVals(entry_LRL, entry_URL, entry_maxSensorRate, entry_fixedAVDelay, 
                var_dynamicAVDelay, var_sensedAVDelayOffset, entry_atrialAmp, entry_ventAmp, entry_atrialWidth, entry_ventWidth, 
                entry_atrialSensit, entry_ventSensit, entry_VRP, entry_ARP, entry_PVARP, var_PVARPext, 
                entry_hysteresis, var_rateSmoothing, entry_ATRDuration, var_ATRFallbackMode, entry_ATRFallbackTime, var_activityThreshold, 
                entry_reactionTime, entry_responseFactor, entry_recoveryTime, mode, userNumber))
            applyButton.place(x=640,y=560, width = 110, height = 30)

            # home button
            homeButton = Button(newCanvas, text = "Home", bg = 'BLACK', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawHomeScreen(modeFrame))
            homeButton.place(x=20,y=20, width = 110, height = 30)

        frame.destroy()

        # making new frame on the window with new canvas on the frame
        homepageFrame = tk.Frame(window, bg="white")
        homepageFrame.pack()

        canvas = Canvas(homepageFrame, width=width, height=height)
        canvas.pack()
        canvas.configure(background='#B5C4D2')
        canvas.create_rectangle(0, 0, 300, height, outline = "", fill = "#FFFFFF")

        # left hand text and image
        canvas.create_text(29, 32, text = "Welcome,", font=("Roboto", 34, "bold"), anchor = NW, fill='black')
        canvas.create_text(29, 90, text = username, font=("Roboto", 34, "bold"), anchor = NW, fill='black')
        canvas.create_image(29, 490, image=smallerLogo, anchor = NW)

        # logout button
        logoutButton = Button(canvas, text = "Sign Out", bg = 'BLACK', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', command=lambda: toWelcome(homepageFrame))
        logoutButton.place(x=1230,y=20, anchor=NE, width = 110, height = 30)

        # available ports drop down
        canvas.create_text(45, 180, text = "Port: ", font=("Roboto", 17), anchor = NW, fill='black')
        global chosenPort
        ports = serial.tools.list_ports.comports()
        listOfPorts = OptionMenu(canvas, chosenPort, "---", *[port.name for port in ports]) # just displays the name of the port
        listOfPorts.config(bg = '#777272', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', highlightcolor = 'BLUE')
        listOfPorts.place(x=115,y=172, anchor=NW, width = 100)

        # refresh button to update the ports dropdown
        refreshButton = Button(canvas, text = "Refresh", bg = 'black', font=("Roboto", 12), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawHomeScreen(homepageFrame))
        refreshButton.place(x=225,y=178, anchor=NW, width = 60, height = 25)

        # sends mode and relevant parameters to pacemaker
        def sendNewMode(sendMode, frame):
            try:
                global currentUserParamObject
                currentUserParamObject.set_sendMode(sendMode)
                save_user_para(userNumber, currentUserParamObject)
                sendParametersToPacemaker(chosenPort.get(),eval("currentUserParamObject."+sendMode+".LRL"), eval("currentUserParamObject."+sendMode+".atrialAmp"), eval("currentUserParamObject."+sendMode+".ventAmp"), eval("currentUserParamObject."+sendMode+".atrialWidth"), eval("currentUserParamObject."+sendMode+".ventWidth"), eval("currentUserParamObject."+sendMode+".ARP"), eval("currentUserParamObject."+sendMode+".VRP"), eval("currentUserParamObject."+sendMode+".reactionTime"), eval("currentUserParamObject."+sendMode+".recoveryTime"), eval("currentUserParamObject."+sendMode+".maxSensorRate"), eval("currentUserParamObject."+sendMode+".responseFactor"), eval("currentUserParamObject."+sendMode+".fixedAVDelay"), eval("currentUserParamObject."+sendMode+".activityThreshold"), currentUserParamObject.sendMode)
                messagebox.showinfo(message="Pacemaker set to mode: "+sendMode+".")
            except:
                checkPort = serial.Serial()
                checkPort.port = chosenPort.get()
                try:
                    checkPort.open()
                    checkPort.close()
                    messagebox.showinfo(message="Pacemaker turned off.")
                except:
                    messagebox.showinfo(message="Pacemaker is no longer connected at this port.")
                drawHomeScreen(homepageFrame)

        # checks if there is a pacemaker connected
        isConnected = connected(chosenPort.get())
        
        if not (isConnected):
            canvas.create_text(30, 230, text = "Pacemaker Disconnected", font=("Roboto", 15, "normal"), anchor = NW, fill='black')
            ports = serial.tools.list_ports.comports() # if nothing connected, lists available ports in text
            
            i = 200
            if (len(ports)):
                canvas.create_text(350, 170, text = "Descriptions of Available Ports:", font=("Roboto", 16, "bold"), anchor = NW, fill='black')
                for port in ports:
                    canvas.create_text(350, i, text = str(port), font=("Roboto", 14, "normal"), anchor = NW, fill='black')
                    i += 30
            else:
                canvas.create_text(350, 170, text = "No available ports detected.", font=("Roboto", 16, "bold"), anchor = NW, fill='black')
            chosenPort.set("---")
        else:
            # information on connected pacemaker
            canvas.create_text(30, 230, text = "Pacemaker Connected", font=("Roboto", 15, "normal"), anchor = NW, fill='black')
            canvas.create_text(30, 255, text = "Pacemaker ID: " + str(chosenPort.get()), font=("Roboto", 15, "normal"), anchor = NW, fill='black')
            canvas.create_text(45, 307, text = "Mode: ", font=("Roboto", 17), anchor = NW, fill='black')
            
            # drop down of possible pacemaker modes to send
            global currentUserParamObject
            sendMode = StringVar(window)
            sendMode.set(currentUserParamObject.get_sendMode())
            listOfModes = OptionMenu(canvas, sendMode, "Off", "AOO", "AAI", "AOOR", "AAIR", "VOO", "VVI", "VOOR", "VVIR", "DOO", "DDD", "DOOR", "DDDR")
            listOfModes.config(bg = '#777272', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', highlightcolor = 'BLUE')
            listOfModes.place(x=115,y=300, anchor=NW, width = 100)

            # button to send a mode to the pacemaker
            sendButton = Button(canvas, text = "Send", bg = 'black', font=("Roboto", 12), borderwidth = 2, fg = 'white', relief='raised', command=lambda: sendNewMode(sendMode.get(), homepageFrame))
            sendButton.place(x=225,y=306, width = 60, height = 25)
                   
            # egram button
            egramButton = Button(canvas, text = "Egram", bg = '#777272', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', command=lambda: egram(homepageFrame))
            egramButton.place(x=320,y=20, anchor=NW, width = 110, height = 30)

            # buttons for each mode
            aooButton = Button(canvas, text = "AOO", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "AOO", "Asynchronous Atrial Pacing"))
            aooButton.place(x=430,y=193.75, width = 200, height = 80, anchor=CENTER)

            aaiButton = Button(canvas, text = "AAI", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "AAI", "Atrial Demand Pacing"))
            aaiButton.place(x=660,y=193.75, width = 200, height = 80, anchor=CENTER)

            aoorButton = Button(canvas, text = "AOOR", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "AOOR", "Rate-Modulated Asynchronous Atrial Pacing"))
            aoorButton.place(x=890,y=193.75, width = 200, height = 80, anchor=CENTER)

            aairButton = Button(canvas, text = "AAIR", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "AAIR", "Rate-Modulated Atrial Demand Pacing"))
            aairButton.place(x=1120,y=193.75, width = 200, height = 80, anchor=CENTER)

            vooButton = Button(canvas, text = "VOO", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "VOO", "Asynchronous Ventricular Pacing"))
            vooButton.place(x=430,y=337.5, width = 200, height = 80, anchor=CENTER)

            vviButton = Button(canvas, text = "VVI", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "VVI", "Ventricular Demand Pacing"))
            vviButton.place(x=660,y=337.5, width = 200, height = 80, anchor=CENTER)

            voorButton = Button(canvas, text = "VOOR", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "VOOR", "Rate-Modulated Asynchronous Ventricular Pacing"))
            voorButton.place(x=890,y=337.5, width = 200, height = 80, anchor=CENTER)

            vvirButton = Button(canvas, text = "VVIR", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "VVIR", "Rate-Modulated Ventricular Demand Pacing"))
            vvirButton.place(x=1120,y=337.5, width = 200, height = 80, anchor=CENTER)

            dooButton = Button(canvas, text = "DOO", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "DOO", "Asynchronous Dual-Chamber Pacing"))
            dooButton.place(x=430,y=481.25, width = 200, height = 80, anchor=CENTER)

            dddButton = Button(canvas, text = "DDD", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "DDD", "Dual-Chamber Demand Pacing"))
            dddButton.place(x=660,y=481.25, width = 200, height = 80, anchor=CENTER)

            doorButton = Button(canvas, text = "DOOR", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "DOOR", "Rate-Modulated Asynchronous Dual-Chamber Pacing"))
            doorButton.place(x=890,y=481.25, width = 200, height = 80, anchor=CENTER)

            dddrButton = Button(canvas, text = "DDDR", bg = '#D44949', font=("Roboto", 34), borderwidth = 2, fg = 'white', relief='raised', command=lambda: drawModeScreen(homepageFrame, "DDDR", "Rate-Modulated Dual-Chamber Demand Pacing"))
            dddrButton.place(x=1120,y=481.25, width = 200, height = 80, anchor=CENTER)

        # called upon click of homepage egram button
        def egram(frame):
            frame.destroy()

            egramFrame = tk.Frame(window, bg="white")
            egramFrame.pack()

            # making canvas on the new egram frame
            egramCanvas = Canvas(egramFrame, width=width, height=height)
            egramCanvas.pack()
            egramCanvas.configure(background='#B5C4D2')
            egramCanvas.create_rectangle(40, 80, width-40, height-50, outline = "", fill = "#FFFFFF")
            
            # plots egram
            plotEgram(egramCanvas, chosenPort.get())

            # have to close the figure when user goes back to homepage
            def onClose(egramFrame):
                plt.close('all')
                drawHomeScreen(egramFrame)
            
            homeButton = Button(egramCanvas, text = "Home", bg = 'BLACK', font=("Roboto", 14), borderwidth = 2, fg = 'white', relief='raised', command=lambda: onClose(egramFrame))
            homeButton.place(x=20,y=20, width = 110, height = 30)
    
    # tries to log in user
    username = user.get()
    password = pswd.get()

    if login_user(username, password)==11 or login_user(username, password)==12:
        messagebox.showinfo(message="Invalid login credentials.")
        toWelcome(frame)
    else:
        # credentials correct, initializes global variable to have current user's parameters
        userNumber = login_user(username, password)
        global currentUserParamObject
        currentUserParamObject = load_user_para(userNumber)
        drawHomeScreen(frame)

# new user page
def newUser(frame):

    # attempts to sign up a new user
    def signUp(user, pswd, frame):
        username = user.get()
        password = pswd.get()
        if num_users()==10:
            messagebox.showinfo(message="Maximum of 10 users reached.")
            toWelcome(frame)
        elif username=="":
            messagebox.showinfo(message="Invalid username.")
            newUser(frame)
        elif check_user(username):
            messagebox.showinfo(message="Username already taken.")
            newUser(frame)
        elif password=="":
            messagebox.showinfo(message="Invalid password.")
            newUser(frame)
        else:
            add_user(username, password)
            messagebox.showinfo(message="New user has been created.")
            toWelcome(frame)
    
    frame.destroy()
    
    # creating frame and canvas for new user page
    newUserFrame = tk.Frame(window, bg="white")
    newUserFrame.pack()
    newUserScreen = Canvas(newUserFrame, width=width, height=height, bg="white")
    newUserScreen.pack()

    # adding logo, text, text entry fields, and buttons
    newUserScreen.create_rectangle(200, 0, width-200, height, outline = "", fill = "#ccc7c6")
    newUserScreen.create_image(625, 154, image=logo)
    newUserScreen.create_text(515, 298, text="Username: ", anchor=NE, font=("Roboto", 34, "bold"), fill="black")
    usernameEntry = tk.Entry(textvariable=username, font=("Roboto", 30))
    newUserScreen.create_window(520, 298, anchor=NW, window=usernameEntry)
    newUserScreen.create_text(515, 358, text="Password: ", anchor=NE, font=("Roboto", 34, "bold"), fill="black")
    passwordEntry = tk.Entry(textvariable=password, font=("Roboto", 30), show="*") 
    newUserScreen.create_window(520, 358, anchor=NW, window=passwordEntry)
    signUpButton = tk.Button(text="Sign Up", font=("Roboto","14"), command=lambda: signUp(username, password, newUserFrame))
    newUserScreen.create_window(width/2, 480, window=signUpButton)
    backButton = tk.Button(text="Login", bg="Black", font=("Roboto","14"), borderwidth=2, fg="white", relief="raised", command=lambda: toWelcome(newUserFrame))
    newUserScreen.create_window(20, 20, width=60, height=30, anchor=NW, window=backButton)

# initial function run upon program start up
def welcome():

    # creating frame and canvas for log in page
    welcomeFrame = tk.Frame(window, bg="white")
    welcomeFrame.pack()
    welcomeScreen = Canvas(welcomeFrame, width=width, height=height, bg="white")
    welcomeScreen.pack()

    # adding logo, text, text entry fields, and buttons to log in page
    welcomeScreen.create_rectangle(200, 0, width-200, height, outline = "", fill = "#B5C4D2")
    welcomeScreen.create_image(width/2, 154, image=logo)
    welcomeScreen.create_text(515, 298, text="Username: ", anchor=NE, font=("Roboto", 34, "bold"), fill="black")
    usernameEntry = tk.Entry(textvariable=username, font=("Roboto", 30)) 
    welcomeScreen.create_window(520, 298, anchor=NW, window=usernameEntry)
    welcomeScreen.create_text(515, 358, text="Password: ", anchor=NE, font=("Roboto", 34, "bold"), fill="black")
    passwordEntry = tk.Entry(textvariable=password, font=("Roboto", 30), show="*") 
    welcomeScreen.create_window(520, 358, anchor=NW, window=passwordEntry)
    loginButton = tk.Button(text="Login", font=("Robotica","14"), command=lambda: homepage(username, password, welcomeFrame))
    welcomeScreen.create_window(width/2, 480, window=loginButton)
    newUserButton = tk.Button(text="Create New User", bg="Black", font=("Roboto","14"), borderwidth=2, fg="white", relief="raised", command=lambda: newUser(welcomeFrame))
    welcomeScreen.create_window(20, 20, width=160, height=30, anchor=NW, window=newUserButton)



# start of program
welcome()
window.mainloop()