import pickle
import check
from tkinter import messagebox

class Parameters:
    def __init__(self, LRL, URL, maxSensorRate, fixedAVDelay, dynamicAVDelay, sensedAVDelayOffset, atrialAmp,
                 ventAmp, atrialWidth, ventWidth, atrialSensit, ventSensit, VRP, ARP, PVARP, PVARPext,
                 hysteresis, rateSmoothing, ATRDuration, ATRFallbackMode, ATRFallbackTime, activityThreshold,
                 reactionTime, responseFactor, recoveryTime):

        self.LRL = LRL
        self.URL = URL
        self.maxSensorRate = maxSensorRate
        self.fixedAVDelay = fixedAVDelay
        self.dynamicAVDelay = dynamicAVDelay
        self.sensedAVDelayOffset = sensedAVDelayOffset
        self.atrialAmp = atrialAmp
        self.ventAmp = ventAmp
        self.atrialWidth = atrialWidth
        self.ventWidth = ventWidth
        self.atrialSensit = atrialSensit
        self.ventSensit = ventSensit
        self.VRP = VRP
        self.ARP = ARP
        self.PVARP = PVARP
        self.PVARPext = PVARPext
        self.hysteresis = hysteresis
        self.rateSmoothing = rateSmoothing
        self.ATRDuration = ATRDuration
        self.ATRFallbackMode = ATRFallbackMode
        self.ATRFallbackTime = ATRFallbackTime
        self.activityThreshold = activityThreshold
        self.reactionTime = reactionTime
        self.responseFactor = responseFactor
        self.recoveryTime = recoveryTime

    def get_activityThreshold(self):
        if (self.activityThreshold == 1):
            return "V-Low"
        elif (self.activityThreshold == 2):
            return "Low"
        elif (self.activityThreshold == 3):
            return "Med-Low"
        elif (self.activityThreshold == 4):
            return "Med"
        elif (self.activityThreshold == 5):
            return "Med-High"
        elif (self.activityThreshold == 6):
            return "High"
        elif (self.activityThreshold == 7):
            return "V-High"
        else:
            return ""

class Modes:
    def __init__(self):
        self.AOO = Parameters(60,120,None,None,None,None,5,None,1,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
        self.AAI = Parameters(60,120,None,None,None,None,5,None,1,None,2.5,None,None,250,250,None,0,0,None,None,None,None,None,None,None)
        self.VOO = Parameters(60,120,None,None,None,None,None,5,None,1,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
        self.VVI = Parameters(60,120,None,None,None,None,None,5,None,1,None,2.5,320,None,None,None,0,0,None,None,None,None,None,None,None)
        self.DOO = Parameters(60,120,None,150,None,None,5,5,1,1,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None)
        self.DDD = Parameters(60,120,None,150,0,0,5,5,1,1,2.5,2.5,320,250,250,0,0,0,20,0,1,None,None,None,None)
        self.AOOR = Parameters(60,120,120,None,None,None,5,None,1,None,None,None,None,None,None,None,None,None,None,None,None,4,30,8,5)
        self.AAIR = Parameters(60,120,120,None,None,None,5,None,1,None,2.5,None,None,250,250,None,0,0,None,None,None,4,30,8,5)
        self.VOOR = Parameters(60,120,120,None,None,None,None,5,None,1,None,None,None,None,None,None,None,None,None,None,None,4,30,8,5)
        self.VVIR = Parameters(60,120,120,None,None,None,None,5,None,1,None,2.5,320,None,None,None,0,0,None,None,None,4,30,8,5)
        self.DOOR = Parameters(60,120,120,150,None,None,5,5,1,1,None,None,None,None,None,None,None,None,None,None,None,4,30,8,5)
        self.DDDR = Parameters(60,120,120,150,0,0,5,5,1,1,2.5,2.5,320,250,250,0,0,0,20,0,1,4,30,8,5)
        self.sendMode = 6

    def set_AOO(self,values):
        self.AOO.LRL = check.LRL(values[0], self.AOO.LRL)
        self.AOO.URL = check.URLmaxSensorRate(values[1], self.AOO.URL, "Upper Rate Limit.")
        self.AOO.atrialAmp = check.ampRegSensit(values[6], self.AOO.atrialAmp, "Atrial Amplitude.")
        self.AOO.atrialWidth = check.width(values[8], self.AOO.atrialWidth, "Atrial Pulse Width.")
        messagebox.showinfo(message="All valid changes have been applied.")
        
    def set_AAI(self,values):
        self.AAI.LRL = check.LRL(values[0], self.AAI.LRL)
        self.AAI.URL = check.URLmaxSensorRate(values[1], self.AAI.URL, "Upper Rate Limit.")
        self.AAI.atrialAmp = check.ampRegSensit(values[6], self.AAI.atrialAmp, "Atrial Amplitude.")
        self.AAI.atrialWidth = check.width(values[8], self.AAI.atrialWidth, "Atrial Pulse Width.")
        self.AAI.atrialSensit = check.ampRegSensit(values[10], self.AAI.atrialSensit, "Atrial Sensitivity.")
        self.AAI.ARP = check.RP(values[13], self.AAI.ARP, "ARP.")
        self.AAI.PVARP = check.RP(values[14], self.AAI.PVARP, "PVARP.")
        self.AAI.hysteresis = check.hysteresis(values[16], self.AAI.hysteresis)
        self.AAI.rateSmoothing = check.dropDownOff(values[17])
        messagebox.showinfo(message="All valid changes have been applied.")
        
    def set_VOO(self,values):
        self.VOO.LRL = check.LRL(values[0], self.VOO.LRL)
        self.VOO.URL = check.URLmaxSensorRate(values[1], self.VOO.URL, "Upper Rate Limit.")
        self.VOO.ventAmp = check.ampRegSensit(values[7], self.VOO.ventAmp, "Ventricular Amplitude.")
        self.VOO.ventWidth = check.width(values[9], self.VOO.ventWidth, "Ventricular Pulse Width.")
        messagebox.showinfo(message="All valid changes have been applied.")

    def set_VVI(self,values):
        self.VVI.LRL = check.LRL(values[0], self.VVI.LRL)
        self.VVI.URL = check.URLmaxSensorRate(values[1], self.VVI.URL, "Upper Rate Limit.")
        self.VVI.ventAmp = check.ampRegSensit(values[7], self.VVI.ventAmp, "Ventricular Amplitude.")
        self.VVI.ventWidth = check.width(values[9],self.VVI.ventWidth, "Ventricular Pulse Width.")
        self.VVI.ventSensit = check.ampRegSensit(values[11], self.VVI.ventSensit, "Ventricular Sensitivity.")
        self.VVI.VRP = check.RP(values[12], self.VVI.VRP, "VRP.")
        self.VVI.hysteresis = check.hysteresis(values[16], self.VVI.hysteresis)
        self.VVI.rateSmoothing = check.dropDownOff(values[17])
        messagebox.showinfo(message="All valid changes have been applied.")

    def set_DOO(self,values):
        self.DOO.LRL = check.LRL(values[0], self.DOO.LRL)
        self.DOO.URL = check.URLmaxSensorRate(values[1], self.DOO.URL, "Upper Rate Limit.")
        self.DOO.fixedAVDelay = check.fixedAVDelay(values[3], self.DOO.fixedAVDelay)
        self.DOO.atrialAmp = check.ampRegSensit(values[6], self.DOO.atrialAmp, "Atrial Amplitude.")
        self.DOO.ventAmp = check.ampRegSensit(values[7], self.DOO.ventAmp, "Ventricular Amplitude.")
        self.DOO.atrialWidth = check.width(values[8], self.DOO.atrialWidth, "Atrial Pulse Width.")
        self.DOO.ventWidth = check.width(values[9], self.DOO.ventWidth, "Ventricular Pulse Width.")
        messagebox.showinfo(message="All valid changes have been applied.")
        
    def set_DDD(self,values):
        self.DDD.LRL = check.LRL(values[0], self.DDD.LRL)
        self.DDD.URL = check.URLmaxSensorRate(values[1], self.DDD.URL, "Upper Rate Limit.")
        self.DDD.fixedAVDelay = check.fixedAVDelay(values[3], self.DDD.fixedAVDelay)
        self.DDD.dynamicAVDelay = check.dropDownOnOff(values[4])
        self.DDD.sensedAVDelayOffset = check.dropDownOff(values[5])
        self.DDD.atrialAmp = check.ampRegSensit(values[6], self.DDD.atrialAmp, "Atrial Amplitude.")
        self.DDD.ventAmp = check.ampRegSensit(values[7], self.DDD.ventAmp, "Ventricular Amplitude.")
        self.DDD.atrialWidth = check.width(values[8], self.DDD.atrialWidth, "Atrial Pulse Width.")
        self.DDD.ventWidth = check.width(values[9], self.DDD.ventWidth, "Ventricular Pulse Width.")
        self.DDD.atrialSensit = check.ampRegSensit(values[10], self.DDD.atrialSensit, "Atrial Sensitivity.")
        self.DDD.ventSensit = check.ampRegSensit(values[11], self.DDD.ventSensit, "Ventricular Sensitivity.")
        self.DDD.VRP = check.RP(values[12], self.DDD.VRP, "VRP.")
        self.DDD.ARP = check.RP(values[13], self.DDD.ARP, "ARP.")
        self.DDD.PVARP = check.RP(values[14], self.DDD.PVARP,"PVARP.")
        self.DDD.PVARPext = check.dropDownOff(values[15])
        self.DDD.hysteresis = check.hysteresis(values[16], self.DDD.hysteresis)
        self.DDD.rateSmoothing = check.dropDownOff(values[17])
        self.DDD.ATRDuration = check.ATRDuration(values[18], self.DDD.ATRDuration)
        self.DDD.ATRFallbackMode = check.dropDownOnOff(values[19])
        self.DDD.ATRFallbackTime = check.ATRFallbackTime(values[20], self.DDD.ATRFallbackTime)
        messagebox.showinfo(message="All valid changes have been applied.")

    def set_AOOR(self,values):
        self.AOOR.LRL = check.LRL(values[0], self.AOOR.LRL)
        self.AOOR.URL = check.URLmaxSensorRate(values[1], self.AOOR.URL, "Upper Rate Limit.")
        self.AOOR.maxSensorRate = check.URLmaxSensorRate(values[2], self.AOOR.maxSensorRate, "Maximum Sensor Rate.")
        self.AOOR.atrialAmp = check.ampRegSensit(values[6], self.AOOR.atrialAmp, "Atrial Amplitude.")
        self.AOOR.atrialWidth = check.width(values[8], self.AOOR.atrialWidth, "Atrial Pulse Width.")
        self.AOOR.activityThreshold = check.activityThreshold(values[21])
        self.AOOR.reactionTime = check.reactionTime(values[22], self.AOOR.reactionTime)
        self.AOOR.responseFactor = check.responseFactor(values[23], self.AOOR.responseFactor)
        self.AOOR.recoveryTime = check.recoveryTime(values[24], self.AOOR.recoveryTime)
        messagebox.showinfo(message="All valid changes have been applied.")
        
    def set_AAIR(self,values):
        self.AAIR.LRL = check.LRL(values[0], self.AAIR.LRL)
        self.AAIR.URL = check.URLmaxSensorRate(values[1], self.AAIR.URL, "Upper Rate Limit.")
        self.AAIR.maxSensorRate = check.URLmaxSensorRate(values[2], self.AAIR.maxSensorRate, "Maximum Sensor Rate.")
        self.AAIR.atrialAmp = check.ampRegSensit(values[6], self.AAIR.atrialAmp, "Atrial Amplitude.")
        self.AAIR.atrialWidth = check.width(values[8], self.AAIR.atrialWidth, "Atrial Pulse Width.")
        self.AAIR.atrialSensit = check.ampRegSensit(values[10], self.AAIR.atrialSensit, "Atrial Sensitivity.")
        self.AAIR.ARP = check.RP(values[13], self.AAIR.ARP, "ARP.")
        self.AAIR.PVARP = check.RP(values[14], self.AAIR.PVARP, "PVARP.")
        self.AAIR.hysteresis = check.hysteresis(values[16], self.AAIR.hysteresis)
        self.AAIR.rateSmoothing = check.dropDownOff(values[17])
        self.AAIR.activityThreshold = check.activityThreshold(values[21])
        self.AAIR.reactionTime = check.reactionTime(values[22], self.AAIR.reactionTime)
        self.AAIR.responseFactor = check.responseFactor(values[23], self.AAIR.responseFactor)
        self.AAIR.recoveryTime = check.recoveryTime(values[24], self.AAIR.recoveryTime)
        messagebox.showinfo(message="All valid changes have been applied.")
        
    def set_VOOR(self,values):
        self.VOOR.LRL = check.LRL(values[0], self.VOOR.LRL)
        self.VOOR.URL = check.URLmaxSensorRate(values[1], self.VOOR.URL, "Upper Rate Limit.")
        self.VOOR.maxSensorRate = check.URLmaxSensorRate(values[2], self.VOO.maxSensorRate, "Maximum Sensor Rate.")
        self.VOOR.ventAmp = check.ampRegSensit(values[7], self.VOOR.ventAmp, "Ventricular Amplitude.")
        self.VOOR.ventWidth = check.width(values[9], self.VOOR.ventWidth, "Ventricular Pulse Width.")
        self.VOOR.activityThreshold = check.activityThreshold(values[21])
        self.VOOR.reactionTime = check.reactionTime(values[22], self.VOOR.reactionTime)
        self.VOOR.responseFactor = check.responseFactor(values[23], self.VOOR.responseFactor)
        self.VOOR.recoveryTime = check.recoveryTime(values[24], self.VOOR.recoveryTime)
        messagebox.showinfo(message="All valid changes have been applied.")
        
    def set_VVIR(self,values):
        self.VVIR.LRL = check.LRL(values[0], self.VVIR.LRL)
        self.VVIR.URL = check.URLmaxSensorRate(values[1], self.VVIR.URL, "Upper Rate Limit.")
        self.VVIR.maxSensorRate = check.URLmaxSensorRate(values[2], self.VVIR.maxSensorRate, "Maximum Sensor Rate.")
        self.VVIR.ventAmp = check.ampRegSensit(values[7], self.VVIR.ventAmp, "Ventricular Amplitude.")
        self.VVIR.ventWidth = check.width(values[9], self.VVIR.ventWidth, "Ventricular Pulse Width.")
        self.VVIR.ventSensit = check.ampRegSensit(values[11], self.VVIR.ventSensit, "Ventricular Sensitivity.")
        self.VVIR.VRP = check.RP(values[12], self.VVIR.VRP, "VRP.")
        self.VVIR.hysteresis = check.hysteresis(values[16], self.VVIR.hysteresis)
        self.VVIR.rateSmoothing = check.dropDownOff(values[17])
        self.VVIR.activityThreshold = check.activityThreshold(values[21])
        self.VVIR.reactionTime = check.reactionTime(values[22], self.VVIR.reactionTime)
        self.VVIR.responseFactor = check.responseFactor(values[23], self.VVIR.responseFactor)
        self.VVIR.recoveryTime = check.recoveryTime(values[24], self.VVIR.recoveryTime)
        messagebox.showinfo(message="All valid changes have been applied.")
        
    def set_DOOR(self,values):
        self.DOOR.LRL = check.LRL(values[0], self.DOOR.LRL)
        self.DOOR.URL = check.URLmaxSensorRate(values[1], self.DOOR.URL, "Upper Rate Limit.")
        self.DOOR.maxSensorRate = check.URLmaxSensorRate(values[2], self.DOOR.maxSensorRate, "Maximum Sensor Rate.")
        self.DOOR.fixedAVDelay = check.fixedAVDelay(values[3], self.DOOR.fixedAVDelay)
        self.DOOR.atrialAmp = check.ampRegSensit(values[6], self.DOOR.atrialAmp, "Atrial Amplitude.")
        self.DOOR.ventAmp = check.ampRegSensit(values[7], self.DOOR.ventAmp, "Ventricular Amplitude.")
        self.DOOR.atrialWidth = check.width(values[8], self.DOOR.atrialWidth, "Atrial Pulse Width.")
        self.DOOR.ventWidth = check.width(values[9], self.DOOR.ventWidth, "Ventricular Pulse Width.")
        self.DOOR.activityThreshold = check.activityThreshold(values[21])
        self.DOOR.reactionTime = check.reactionTime(values[22], self.DOOR.reactionTime)
        self.DOOR.responseFactor = check.responseFactor(values[23], self.DOOR.responseFactor)
        self.DOOR.recoveryTime = check.recoveryTime(values[24], self.DOOR.recoveryTime)
        messagebox.showinfo(message="All valid changes have been applied.")

    def set_DDDR(self,values):
        self.DDDR.LRL = check.LRL(values[0], self.DDDR.LRL)
        self.DDDR.URL = check.URLmaxSensorRate(values[1], self.DDDR.URL, "Upper Rate Limit.")
        self.DDDR.maxSensorRate = check.URLmaxSensorRate(values[2], self.DDDR.maxSensorRate, "Maximum Sensor Rate.")
        self.DDDR.fixedAVDelay = check.fixedAVDelay(values[3], self.DDDR.fixedAVDelay)
        self.DDDR.dynamicAVDelay = check.dropDownOnOff(values[4])
        self.DDDR.sensedAVDelayOffset = check.dropDownOff(values[5])
        self.DDDR.atrialAmp = check.ampRegSensit(values[6], self.DDDR.atrialAmp, "Atrial Amplitude.")
        self.DDDR.ventAmp = check.ampRegSensit(values[7], self.DDDR.ventAmp, "Ventricular Amplitude.")
        self.DDDR.atrialWidth = check.width(values[8], self.DDDR.atrialWidth, "Atiral Pulse Width.")
        self.DDDR.ventWidth = check.width(values[9], self.DDDR.ventWidth, "Ventricular Pulse Width.")
        self.DDDR.atrialSensit = check.ampRegSensit(values[10], self.DDDR.atrialSensit, "Atrial Sensitivity.")
        self.DDDR.ventSensit = check.ampRegSensit(values[11], self.DDDR.ventSensit, "Ventricular Sensitivity.")
        self.DDDR.VRP = check.RP(values[12], self.DDDR.VRP, "VRP.")
        self.DDDR.ARP = check.RP(values[13], self.DDDR.ARP, "ARP.")
        self.DDDR.PVARP = check.RP(values[14], self.DDDR.PVARP, "PVARP.")
        self.DDDR.PVARPext = check.dropDownOff(values[15])
        self.DDDR.hysteresis = check.hysteresis(values[16], self.DDDR.hysteresis)
        self.DDDR.rateSmoothing = check.dropDownOff(values[17])
        self.DDDR.ATRDuration = check.ATRDuration(values[18], self.DDDR.ATRDuration)
        self.DDDR.ATRFallbackMode = check.dropDownOnOff(values[19])
        self.DDDR.ATRFallbackTime = check.ATRFallbackTime(values[20], self.DDDR.ATRFallbackTime)
        self.DDDR.activityThreshold = check.activityThreshold(values[21])
        self.DDDR.reactionTime = check.reactionTime(values[22], self.DDDR.reactionTime)
        self.DDDR.responseFactor = check.responseFactor(values[23], self.DDDR.responseFactor)
        self.DDDR.recoveryTime = check.recoveryTime(values[24], self.DDDR.recoveryTime)
        messagebox.showinfo(message="All valid changes have been applied.")
    
    def set_sendMode(self, mode):
        self.sendMode = check.sendMode(mode)
        
    def get_sendMode(self):
        if (self.sendMode == 0):
            return "Off"
        elif (self.sendMode == 1):
            return "AOO"
        elif (self.sendMode == 2):
            return "AAI"
        elif (self.sendMode == 3):
            return "VOO"
        elif (self.sendMode == 4):
            return "VVI"
        elif (self.sendMode == 5):
            return "DOO"
        elif (self.sendMode == 6):
            return "DDD"
        elif (self.sendMode == 7):
            return "AOOR"
        elif (self.sendMode == 8):
            return "AAIR"
        elif (self.sendMode == 9):
            return "VOOR"
        elif (self.sendMode == 10):
            return "VVIR"
        elif (self.sendMode == 11):
            return "DOOR"
        elif (self.sendMode == 12):
            return "DDDR"

def create_new_user_para():
    user = Modes()
    return user

# uses pickle to load users from file
def load_users():
    try:
        infile = open("users.pkl", 'rb')
        users = pickle.load(infile)
        infile.close()
        return users
    except FileNotFoundError:
        users = [0]
        outfile = open("users.pkl",'wb')
        pickle.dump(users, outfile)
        outfile.close()
        return users

# saves users with pickle
def save_users(users):
    outfile = open("users.pkl",'wb')
    pickle.dump(users, outfile)
    outfile.close()
    return 1

def check_user(username):
    users = load_users()
    
    if users[0] == 0:
        return False
    else:
        for user in users[1:]:
            if username == user[0]:
                return True
        return False

def num_users():
    users = load_users()
    return users[0]    

def add_user(username, password):
    users = load_users()
    users[0] += 1
    users.append([username,password])
    user_para = create_new_user_para()
    save_users(users)
    save_user_para(str(users[0]),user_para)

def login_user(input_user, password):  ## Returns integer 1 - 10 if login succesful (integer corresponds to user data), 11 if wrong pw, 12 if no username
    users = load_users()
    user_num = 0
    for username in users[1:]:
        user_num += 1
        if input_user == username[0]:
            if password == username[1]:
                return user_num
            else:
                return 11
    return 12

# load user's object from file with pickle
def load_user_para(user):
    infile = open("user" + str(user) + ".pkl", 'rb')
    obj = pickle.load(infile)
    infile.close()
    return obj

# saves user's object to file with pickle
def save_user_para(user, obj):
    outfile = open("user" + str(user) + ".pkl", 'wb')
    pickle.dump(obj, outfile)
    outfile.close()
    return 1