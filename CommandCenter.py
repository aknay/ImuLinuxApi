__author__ = 'aknay'
import Commands
from SerialPort import SerialPort
import struct
from time import sleep

class CommandCenter:
    def __init__(self, portName):
        self.portName = portName
        self.serialLink = SerialPort(self.portName)

    def getTaredOrientationAsQuaternion(self, sensorId):
        data = self.__getWirelessBinaryCommand(Commands.GET_TARED_QUAT, sensorId)
        self.__sendDataToSerialPort(data)
        return self.__getFormatedDataFromSerialPort(lengthOfPacket=19,format=">ffff")

    def setStreamingTiming (self,interval,duration,delay, sensorId):
        commandData = [0.0] * 3
        commandData[0] = interval
        commandData[1] = duration
        commandData[2] = delay
        data = self.__getWirelessBinaryCommand(Commands.SET_STREAMING_TIMING,sensorId,commandData=commandData,format=">III")
        self.__retryIfSetCommandFailed(data,"setStreamingTiming", sensorId=sensorId)


    def getOffsetQuaternion(self,sensorId):
        self.__getNorthAndGravityVectorsInSensorFrame(sensorId)
        self.__getUntaredOrientationAsQuaternion(sensorId)


    def getThisData(self):
        numberOfByteAvaialbe = self.serialLink.getNumberOfByteAvailable()
        if numberOfByteAvaialbe>18:
            receivedData = self.serialLink.readData(numberOfByteAvaialbe)
            if (numberOfByteAvaialbe == 19):
                formatedData = self.__getFormatedData(receivedData,format=">ffff")
                return formatedData
        EmptyList = list()
        return EmptyList


    def getTaredOridntationAsQuaternionFromBuffer(self, sensorId):
        print (self.serialLink.getNumberOfByteAvailable())

    def getSerialBuffer(self):
        print("the buffer is")
        print ("available number of Byte")
        print (self.serialLink.getNumberOfByteAvailable())

        print repr(self.serialLink.readData(self.serialLink.getNumberOfByteAvailable()))
        print ("available number of Byte after read")
        print (self.serialLink.getNumberOfByteAvailable())


    def closeSerialPort(self):
        self.serialLink.clostPort()


    def setStreamingSlot(self,sensorId, slot1, slot2 = chr(0xff),slot3 = chr(0xff), slot4= chr(0xff), slot5= chr(0xff), slot6= chr(0xff),slot7= chr(0xff),slot8= chr(0xff)):
        commandData = [0.0] * 8
        commandData[0] = slot1
        commandData[1] = slot2
        commandData[2] = slot3
        commandData[3] = slot4
        commandData[4] = slot5
        commandData[5] = slot6
        commandData[6] = slot7
        commandData[7] = slot8
        data = self.__getWirelessBinaryCommand(Commands.SET_STREAMING_SLOTS,sensorId, commandData=commandData,format='cccccccc')
        self.__retryIfSetCommandFailed(data,"setStreamingSlots", sensorId=sensorId)



    def startStreaming(self, sensorId):
        data = self.__getWirelessBinaryCommand(Commands.START_STREAMING, sensorId)
        self.__sendDataToSerialPort(data)
        self.__retryIfSetCommandFailed(data,"StartStreaming", sensorId=sensorId)

    def stopStreaming(self,sensorId):
        data = self.__getWirelessBinaryCommand(Commands.STOP_STREAMING, sensorId)
        self.__sendDataToSerialPort(data)
        self.__retryIfSetCommandFailed(data,"StopStreaming", sensorId=sensorId)

    def getStreamingTiming(self,sensorId):
        data = self.__getWirelessBinaryCommand(Commands.GET_STREAMING_TIMING, sensorId)
        self.__sendDataToSerialPort(data)
        return self.__getFormatedDataFromSerialPort(lengthOfPacket=15,format="III")



















########################################################################################################################
#Private function


    def __getUntaredOrientationAsQuaternion(self, sensorId):
        command = Commands.getCommandAsChr(Commands.GET_UNTARED_ORIENTATION_AS_QUATERNION)
        lengthOfReturnData = Commands.getReturnDataLength(Commands.GET_UNTARED_ORIENTATION_AS_QUATERNION)
        binaryCommand = self.__getWirelessBinaryCommand(command, sensorId)
        receivedData = self.__getRawDataAndRetryIfGetCommandFailed(sensorId,binaryCommand,lengthOfReturnData)
        print (self.__getFormatedData(receivedData,format = ">ffff"))


    def __getNorthAndGravityVectorsInSensorFrame(self, sensorId):
        command = Commands.getCommandAsChr(Commands.GET_NORTH_AND_GRAVITY_VECTORS_IN_SENSOR_FRAME)
        lengthOfReturnData = Commands.getReturnDataLength(Commands.GET_NORTH_AND_GRAVITY_VECTORS_IN_SENSOR_FRAME)
        binaryCommand = self.__getWirelessBinaryCommand(command, sensorId)
        receivedData = self.__getRawDataAndRetryIfGetCommandFailed(sensorId,binaryCommand,lengthOfReturnData)
        print (self.__getFormatedData(receivedData,format = ">ffffff"))


    def __getRawDataAndRetryIfGetCommandFailed(self,sensorId,binaryCommand, returnDataLength):
        print("in retry")
        WIRELESS_HEADER_LENGTH = 3
        SUCESSFULLY_SENT = chr(0x00)
        TOTAL_PACKET_LENGTH = WIRELESS_HEADER_LENGTH + returnDataLength
        self.__sendDataToSerialPort(binaryCommand)
        receivedData = (self.serialLink.readData(TOTAL_PACKET_LENGTH))
        print repr(receivedData)

        while receivedData[0] != SUCESSFULLY_SENT and receivedData[1] != sensorId and receivedData != returnDataLength:
            print "fail"
            self.serialLink.flushBuffer()
            self.__sendDataToSerialPort(binaryCommand)
            receivedData = (self.serialLink.readData(TOTAL_PACKET_LENGTH))
        print("sucessful")
        return receivedData





    def __getFormatedData(self, data, format):
        actualData = data[3:len(data)]
        sensorId = data[1]
        dataToBeReturned = list(struct.unpack(format, actualData))
        dataToBeReturned.insert(0,ord(sensorId))
        return dataToBeReturned

        #list(struct.unpack(format, actualData))
        #list.append(0,sensorId)
        #return list(struct.unpack(format, actualData))
        #list.append((data[2])
        #print
        #return (data[2],list(str(struct.unpack(format, actualData))))
        #return list(str(struct.unpack(format, actualData)))

    def __getSensorId(self,data):
        return data[1]



    def __flushBuffer(self):
        self.serialLink.readData(self.serialLink.getNumberOfByteAvailable())
        self.serialLink.flushBuffer()

    def __retryIfSetCommandFailed(self, data, nameOfCommand, sensorId):
        self.__sendDataToSerialPort(data)
        while self.__isCommandSuccessful(sensorId) == False:
            self.__flushBuffer()
            print ("going to send again")
            self.__sendDataToSerialPort(data)
        print (nameOfCommand + " command is successfully sent to sensor ID: " + str(sensorId))

    def __isCommandSuccessful(self, sensorId):
        print(self.serialLink.getNumberOfByteAvailable())
        numberOfbyte =  self.serialLink.getNumberOfByteAvailable()
        print (numberOfbyte)
        receivedData = (self.serialLink.readData(3))
        if ((receivedData[0] == chr(0x00))and(receivedData[1]==chr(int(sensorId)))):
            print ("command successful" + repr(receivedData))
            return True
        else:
            # print repr(receivedData)
            print ("command failed" + repr(receivedData))
            return False

    def __getFormatedDataFromSerialPort(self, lengthOfPacket, format):
        receivedData = (self.serialLink.readData(lengthOfPacket))
        if receivedData[0] == chr(0x00):
            print "successful"
            actualData = receivedData[3:lengthOfPacket]
            outputData = list(struct.unpack(format, actualData))
            return outputData
        else:
            print("data not avaialbe yet" + repr(receivedData))
            return None

    def __sendDataToSerialPort(self, data):
        self.serialLink.sendData(data)

    def __getWirelessBinaryCommand(self, command, sensorId, commandData=[], format=""):
        sensorId = chr(int(sensorId))
        if len(commandData) > 0:
            packedData = struct.pack(format, *commandData)
            sendingData = Commands.WIRELESS_STARTING_BYTE + sensorId + command + packedData + self.__getCheckSum(
                sensorId + command + packedData)
            return sendingData

        else:
            sendingData = Commands.WIRELESS_STARTING_BYTE + sensorId + command + self.__getCheckSum(
                sensorId + command)
            return sendingData

    def __getCheckSum(self, char_data):
        """ Calculates the checksum for the given data.
            Args: char_data: A string of data.
        """
        checksum = 0
        for byte in char_data:
            checksum += ord(byte)
        return chr(checksum % 256)
