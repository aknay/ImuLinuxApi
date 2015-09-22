__author__ = 'root'
__author__ = 'root'
import ListOfCommands
from SerialPort import SerialPort
import struct

class CommandCenter:
    def __init__(self, portName):
        self.portName = portName
        self.serialLink = SerialPort(self.portName)

    def getTaredOrientationAsQuaternion(self, sensorId):
        data = self.__packWirelessCommandData(ListOfCommands.GET_TARED_QUAT, sensorId)
        self.__sendData(data)
        return self.__getFormatedDataFromSerialPort(lengthOfPacket=19,format=">ffff")


    #TO DO
    def setStreamingTiming (self,interval,druation,delay, sensorId):
        commandData = [0.0] * 3
        commandData[0] = interval
        commandData[1] = druation
        commandData[2] = delay
        data = self.__packWirelessCommandData(ListOfCommands.SET_STREAMING_TIMING,sensorId,commandData=commandData,format=">III")
        print repr(data)
        self.__sendData(data)
        self.isCommandFail()


    def isCommandFail (self):
        receivedData = (self.serialLink.readData(2))
        if receivedData[0] == chr(0x00):
            print "successful"
        else:
            print repr(receivedData)
            print "fail"

    def startStreaming(self, sensorId):
        data = self.__packWirelessCommandData(ListOfCommands.START_STREAMING, sensorId)
        self.__sendData(data)

    def stopStreaming(self,sensorId):
        data = self.__packWirelessCommandData(ListOfCommands.STOP_STREAMING, sensorId)
        self.__sendData(data)

    def getStreamingTiming(self,sensorId):
        data = self.__packWirelessCommandData(ListOfCommands.GET_STREAMING_TIMING, sensorId)
        self.__sendData(data)
        return self.__getFormatedDataFromSerialPort(lengthOfPacket=15,format="III")

    def __getFormatedDataFromSerialPort(self,lengthOfPacket,format):
        receivedData = (self.serialLink.readData(lengthOfPacket))
        if receivedData[0] == chr(0x00):
            print "successful"
            actualData = receivedData[3:lengthOfPacket]
            outputData = list(struct.unpack(format, actualData))
            return outputData
        else:
            print("something wrong")
            return None

    def __sendData(self, data):
        self.serialLink.sendData(data)

    def __packWirelessCommandData(self,command, sensorId, commandData=[], format=""):
        sensorId = chr(int(sensorId))
        if len(commandData)>0:
            packedData = struct.pack(format,*commandData)
            print repr(packedData)
            sendingData = ListOfCommands.WIRELESS_STARTING_BYTE+sensorId + command+packedData+self.__getCheckSum(sensorId+command+packedData)
            print repr(sendingData)
            return sendingData

        else:
            sendingData = ListOfCommands.WIRELESS_STARTING_BYTE + sensorId + command + self.__getCheckSum(sensorId + command)
            print("data")
            return sendingData

    def __getCheckSum(self,char_data):
        """ Calculates the checksum for the given data.
            Args: char_data: A string of data.
        """
        checksum = 0
        for byte in char_data:
            checksum += ord(byte)
        return chr(checksum % 256)