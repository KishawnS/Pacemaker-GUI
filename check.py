from tkinter import messagebox

# check functions for each parameter to validate the value the user entered before they are saved or sent
# if they are invalid values, the functions try to return the closest valid value
# if this cannot be done, an error message is returned

def LRL(value, currentValue):
    try: 
        value = int(value)
        if value < 30:
            return 30
        elif value > 175:
            return 175
        elif value < 50:
            return round(5*round(value/5))
        elif value < 90:
            return round(1*round(value/1))
        else:
            return round(5*round(value/5))
    except:
        messagebox.showinfo(message="Please enter a valid integer in Lower Rate Limit.")
        return currentValue
    
def URLmaxSensorRate(value, currentValue, field):
    try: 
        value = int(value)
        if value < 50:
            return 50
        elif value > 175:
            return 175
        else:
            return round(5*round(value/5))
    except:
        messagebox.showinfo(message="Please enter a valid integer in " + field)
        return currentValue

def fixedAVDelay(value, currentValue):
    try:
        value = int(value)
        if value < 70:
            return 70
        elif value > 300:
            return 300
        else:
            return round(10*round(value/10))
    except:
        messagebox.showinfo(message="Please enter a valid integer in Fixed AV Delay.")
        return currentValue

def dropDownOnOff(value):
    if value == "On":
        return 1
    else:
        return 0

def dropDownOff(value):
    if value == "Off":
        return 0
    else:
        return value

def ampRegSensit(value, currentValue, field):
    try: 
        value = float(value)
        if value < 0:
            return 0
        elif value > 5:
            return 5
        else:
            return round(0.1*round(value/0.1),1)
    except:
        messagebox.showinfo(message="Please enter a valid decimal number in " + field)
        return currentValue

def ampUnReg(value, currentValue, field):
    try:
        value = float(value)
        if value < 0:
            return 0
        elif value > 5:
            return 5
        else:
            return round(1.25*round(value/1.25),2)
    except:
        messagebox.showinfo(message="Please enter a valid decimal number in " + field)
        return currentValue
    
def width(value, currentValue, field):
    try:
        value = int(value)
        if value < 1:
            return 1
        elif value > 30:
            return 30
        else:
            return round(1*round(value/1))
    except:
        messagebox.showinfo(message="Please enter a valid integer in " + field)
        return currentValue
        
def RP(value, currentValue, field):
    try:
        value = int(value)
        if value < 150:
            return 150
        elif value > 500:
            return 500
        else:
            return round(10*round(value/10))
    except:
        messagebox.showinfo(message="Please enter a valid integer in " + field)
        return currentValue

def hysteresis(value, currentValue):
    try: 
        value = int(value)
        if value < 15:
            return 0
        elif value > 175:
            return 175
        elif value < 30:
            return 30
        elif value < 50:
            return round(5*round(value/5))
        elif value < 90:
            return round(1*round(value/1))
        else:
            return round(5*round(value/5))
    except:
        messagebox.showinfo(message="Please enter a valid integer in Hysteresis.")
        return currentValue

def ATRDuration(value, currentValue):
    try:
        value = int(value)
        if value < 0:
            return 0
        elif value > 2000:
            return 2000
        elif value < 15:
            return 10
        elif value < 90:
            return round(20*round(value/20))
        else:
            return round(100*round(value/100))
    except:
        messagebox.showinfo(message="Please enter a valid integer in ATR Duration.")
        return currentValue

def ATRFallbackTime(value, currentValue):
    try:
        value = int(value)
        if value < 1:
            return 1
        elif value > 5:
            return 5
        else:
            return value
    except:
        messagebox.showinfo(message="Please enter a valid integer in ATR Fallback Time.")
        return currentValue
    
def activityThreshold(value):
    if value == "V-Low":
        return 1
    elif value == "Low":
        return 2
    elif value == "Med-Low":
        return 3
    elif value == "Med":
        return 4
    elif value == "Med-High":
        return 5
    elif value == "High":
        return 6
    elif value == "V-High":
        return 7
    else:
        return 4

def reactionTime(value, currentValue):
    try:
        value = int(value)
        if value < 10:
            return 10
        elif value > 50:
            return 50
        else:
            return round(10*round(value/10))
    except:
        messagebox.showinfo(message="Please enter a valid integer in Reaction Time.")
        return currentValue

def responseFactor(value, currentValue):
    try:
        value = int(value)
        if value < 1:
            return 1
        elif value > 16:
            return 16
        else:
            return value
    except:
        messagebox.showinfo(message="Please enter a valid integer in Response Factor.")
        return currentValue

def recoveryTime(value,currentValue):
    try:
        value = int(value)
        if value < 2:
            return 2
        elif value > 16:
            return 16
        else:
            return value
    except:
        messagebox.showinfo(message="Please enter a valid integer in Recovery Time.")
        return currentValue
    
def sendMode(value):
    if value == "Off":
        return 0
    elif value == "AOO":
        return 1
    elif value == "AAI":
        return 2
    elif value == "VOO":
        return 3
    elif value == "VVI":
        return 4
    elif value == "DOO":
        return 5
    elif value == "DDD":
        return 6
    elif value == "AOOR":
        return 7
    elif value == "AAIR":
        return 8
    elif value == "VOOR":
        return 9
    elif value == "VVIR":
        return 10
    elif value == "DOOR":
        return 11
    elif value == "DDDR":
        return 12
    else:
        return 6