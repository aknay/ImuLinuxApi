__author__ = 'aknay'
WIRELESS_STARTING_BYTE = chr(0xf8)
#GET_TARED_ORIENTATION_AS_QUATERNION = chr(0x00)
GET_STREAMING_TIMING = chr(0x53)
START_STREAMING = chr(0x55)
STOP_STREAMING = chr(0x56)
SET_STREAMING_TIMING = chr(0x52)
SET_STREAMING_SLOTS = chr (0x50)

#----------------The Format Of Command------------------------------
#commandAsChar, ReturnDataLength,ReturnDataFormat, DataLenght,DataFormat

GET_TARED_ORIENTATION_AS_QUATERNION = [chr(0x00),16,'>ffff',0,None]

GET_UNTARED_ORIENTATION_AS_QUATERNION = [chr(0x06),16,">ffff",0,None]
GET_NORTH_AND_GRAVITY_VECTORS_IN_SENSOR_FRAME = [chr(0x0c),24,">ffffff",0,None]
TARE_WITH_QUATERNION = [chr(0x61),0,None,16,'>ffff']


#Only For Streaming Command
SLOT_GET_TARED_QUAT = chr(0x00)

def getCommandAsChr(command):
    return command[0]

def getReturnDataLength(command):
    return command[1]

def getRetrunDataFormat(command):
    return command[2]

def getDataLength(command):
    return command[3]

def getDataFormat(command):
    return command[4]