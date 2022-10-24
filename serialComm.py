import serial
import struct

# returns whether or not a successful connection to the user's chosen serial communcation port could be made
def connected(chosenPort):
    try:
        sercom = serial.Serial()
        sercom.baudrate = 115200 # instructed to use
        sercom.port = chosenPort
        sercom.open()
        return(sercom.is_open)
    except:
        return False

# converts a float into a list of four bytes
def floatToBytearray(float):
    ba = struct.pack("<f", float)
    byteList = []
    for int in ba:
        byteList.append(int.to_bytes(1, "little"))
    return byteList

# converts four bytes to float
def bytearrayToFloat(bytearray):
    return round(struct.unpack('<f', bytearray)[0],2)

# converts eight bytes to double
def bytearrayToDouble(bytearray):
    return struct.unpack('<d', bytearray)[0]

# converts 14 parameter values to bytes and sends to pacemaker
def sendParametersToPacemaker(portName, LRL, atrAMP, ventAMP, atrPulseWidth, ventPulseWidth, ARP, VRP, reaction, recovery, maxSensorRate, responseFactor, fixedAVDelay, activityThreshold, sendMode):
    # list of all parameter values (exclues portName parameter)
    args = [LRL, atrAMP, ventAMP, atrPulseWidth, ventPulseWidth, ARP, VRP, reaction, recovery, maxSensorRate, responseFactor, fixedAVDelay, activityThreshold, sendMode]
    # the disabled fields for a mode would have sent "none" values. All "none" values must be converted into 0s before we send to the pacemaker.
    for i in range(14):
        if (args[i] == None):
            args[i] = 0
        
    # packing all parameters as list of bytes to be sent to parameter
    packet = []
    packet.append(b'\x16')
    packet.append(b'\x55') # parameter looks out for 16 and 55 to mean we are sending it values
    packet.append(args[0].to_bytes(1, "little"))
    packet += floatToBytearray(args[1])
    packet += floatToBytearray(args[2])
    packet.append(args[3].to_bytes(1, "little"))
    packet.append(args[4].to_bytes(1, "little"))
    packet += [args[5].to_bytes(2, "little")]
    packet += [args[6].to_bytes(2, "little")]
    packet.append(args[7].to_bytes(1, "little"))
    packet.append(args[8].to_bytes(1, "little"))
    packet.append(args[9].to_bytes(1, "little"))
    packet.append(args[10].to_bytes(1, "little"))
    packet += [args[11].to_bytes(2, "little")]
    packet.append(args[12].to_bytes(1, "little"))
    packet.append(args[13].to_bytes(1, "little"))

    # opens communication at user's chosen port
    sercom = serial.Serial()
    sercom.baudrate = 115200
    sercom.port = portName

    sercom.open()
    
    # send all bytes
    for pack in packet:
        sercom.write(pack)

    sercom.close()


# receives 39 bytes from the pacemaker and converts them into 16 values to be used by DCM
def receiveParametersFromPacemaker(portName):

    # opens communication at user's chosen port
    sercom = serial.Serial()
    sercom.baudrate = 115200
    sercom.port = portName

    sercom.open()

    # to request data from the pacemaker, we have to firstly send 16 and 22
    packet = []
    packet.append(b'\x16')
    packet.append(b'\x22')

    for i in range(23):
        packet.append(b'\x00')

    # sending packet
    for pack in packet:
        sercom.write(pack)

    # reading the correct amount of bytes for the data type to each index of a new array
    returnedByteArray = []
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(4))
    returnedByteArray.append(sercom.read(4))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(2))
    returnedByteArray.append(sercom.read(2))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(2))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(1))
    returnedByteArray.append(sercom.read(8))
    returnedByteArray.append(sercom.read(8))

    sercom.close()

    # taking the bytes at each index of our byte array and converting them into the correct data type
    convertedArray = []

    convertedArray.append(int.from_bytes(returnedByteArray[0], "little"))
    convertedArray.append(bytearrayToFloat(returnedByteArray[1]))
    convertedArray.append(bytearrayToFloat(returnedByteArray[2]))
    for i in range(11):
        convertedArray.append(int.from_bytes(returnedByteArray[i+3], "little"))
    convertedArray.append(bytearrayToDouble(returnedByteArray[14]))
    convertedArray.append(bytearrayToDouble(returnedByteArray[15]))

    # returns the array of integers, floats and doubles
    return convertedArray