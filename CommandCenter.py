__author__ = 'aknay'
import Commands
from SerialPort import SerialPort
import struct
from VectorAndQuaternionCalculator import VectorAndQuaternionCalculator
from time import sleep

class CommandCenter:
    def __init__(self, portName):
        self.portName = portName
        self.serialLink = SerialPort(self.portName)

        #binaryCommand = self.__getWirelessBinaryCommand(command, sensorId)
        #self.__sendDataToSerialPort(binaryCommand)
        #return self.__getFormatedDataFromSerialPort(lengthOfPacket=19,format)

    def setStreamingTiming (self,interval,duration,delay, sensorId):
        commandData = [0.0] * 3
        commandData[0] = interval
        commandData[1] = duration
        commandData[2] = delay
        data = self.__getWirelessBinaryCommand(Commands.SET_STREAMING_TIMING,sensorId,commandData=commandData,format=">III")
        self.__retryIfSetCommandFailed(data,"setStreamingTiming", sensorId=sensorId)


    def performOffsetOperation(self,sensorId):

        #we are trying to find offset here by getting gravity vector of device and gravity vector that we want it as
        northAndGravityVectors = self.__getNorthAndGravityVectorsInSensorFrame(sensorId)
        untaredOrientationAsQuaternion = self.__getUntaredOrientationAsQuaternion(sensorId,needToReturnSensorId=False)
        vectorAndQuaternionCalculator = VectorAndQuaternionCalculator()
        offsetAsQuaternion = vectorAndQuaternionCalculator.getOffsetOrientationAsQuaternion(northAndGravityVectors)

        #below two statements is to offset gd so that it is align with g
        taredData = vectorAndQuaternionCalculator.getMultiplicationOfQuaternion(untaredOrientationAsQuaternion,offsetAsQuaternion)
        self.__setTareOrientationAsSameAsSuppliedOrientationInQuaternionDomain(sensorId,tareData=taredData)

        return offsetAsQuaternion



    def getAngleBetweenThreeVectors(self, vectorOne,vectorTwo,vectorthree):
        vectorAndQuaternionCalculator = VectorAndQuaternionCalculator()
        return vectorAndQuaternionCalculator.calculateAngle(vectorOne,vectorTwo,vectorthree)


    def getDeviceVector(self,sensorId, suppliedVector, offsetAsQuaternion):
        taredOrientationAsQuaternion =  self.__getTaredOrientationAsQuaternion(sensorId,needToReturnSensorId=False)
        #print "taredOrientationAsQuaternion"
        #print taredOrientationAsQuaternion

        vectorAndQuaternionCalculator = VectorAndQuaternionCalculator()
        vector = vectorAndQuaternionCalculator.getVectorOftheDeviceBasedOnSuppliedOrientation(suppliedVector,taredOrientationAsQuaternion,offsetAsQuaternion)
        return vector

    def calculateDeviceVector(self,sensorId,vector,offset):
        taredOrientationAsQuaternion =  self.__getTaredOrientationAsQuaternion(sensorId)
        ## Apply the offset for the device
        quat = self.__quaternionMultiplication(taredOrientationAsQuaternion, offset)
        ## Calculate a vector for the device with its orientation
        vector = self.__quaternionVectorMultiplication(quat, vector)
        return vector


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
        binaryCommand = self.__getWirelessBinaryCommand(Commands.START_STREAMING, sensorId)
        self.__sendDataToSerialPort(binaryCommand)
        self.__retryIfSetCommandFailed(binaryCommand,"StartStreaming", sensorId=sensorId)

    def stopStreaming(self,sensorId):
        binaryCommand = self.__getWirelessBinaryCommand(Commands.STOP_STREAMING, sensorId)
        self.__sendDataToSerialPort(binaryCommand)
        self.__retryIfSetCommandFailed(binaryCommand,"StopStreaming", sensorId=sensorId)

    def getStreamingTiming(self,sensorId):
        binaryCommand = self.__getWirelessBinaryCommand(Commands.GET_STREAMING_TIMING, sensorId)
        self.__sendDataToSerialPort(binaryCommand)
        return self.__getFormatedDataFromSerialPort(lengthOfPacket=15,format="III")

########################################################################################################################
#Private function

    def __getTaredOrientationAsQuaternion(self, sensorId,needToReturnSensorId = True):
        command = Commands.getCommandAsChr(Commands.GET_TARED_ORIENTATION_AS_QUATERNION)
        format = Commands.getRetrunDataFormat(Commands.GET_TARED_ORIENTATION_AS_QUATERNION)
        lengthOfReturnData = Commands.getReturnDataLength(Commands.GET_TARED_ORIENTATION_AS_QUATERNION)
        binaryCommand = self.__getWirelessBinaryCommand(command, sensorId)
        receivedData = self.__getRawDataAndRetryIfGetCommandFailed(sensorId,binaryCommand,lengthOfReturnData)

        if needToReturnSensorId is True:
            return (self.__getFormatedData(receivedData,format))
        else:
            return (self.__getFormatedDataWithoutSensorId(receivedData,format))

    def __setTareOrientationAsSameAsSuppliedOrientationInQuaternionDomain(self, sensorId, tareData):
        command = Commands.getCommandAsChr(Commands.TARE_WITH_QUATERNION)
        dataFormat = Commands.getDataFormat(Commands.TARE_WITH_QUATERNION)

        binaryCommand = self.__getWirelessBinaryCommand(command, sensorId, tareData, dataFormat)
        self.__retryIfSetCommandFailed(binaryCommand,"tareWithQuaternion", sensorId=sensorId)

    def __getUntaredOrientationAsQuaternion(self, sensorId = 0,needToReturnSensorId = True):
        command = Commands.getCommandAsChr(Commands.GET_UNTARED_ORIENTATION_AS_QUATERNION)
        lengthOfReturnData = Commands.getReturnDataLength(Commands.GET_UNTARED_ORIENTATION_AS_QUATERNION)
        format = Commands.getRetrunDataFormat(Commands.GET_UNTARED_ORIENTATION_AS_QUATERNION)

        binaryCommand = self.__getWirelessBinaryCommand(command, sensorId)
        receivedData = self.__getRawDataAndRetryIfGetCommandFailed(sensorId,binaryCommand,lengthOfReturnData)
        if needToReturnSensorId is True:
            return (self.__getFormatedData(receivedData,format))
        else:
            #Note: starting byte is sensorId followed by data, need to remove index 0 if you dont want to get sensorId as return data
            return (self.__getFormatedData(receivedData,format))[1:]


    def __getFormatedDataWithoutSensorId(self,data, format):
        actualData = data[3:len(data)]
        dataToBeReturned = list(struct.unpack(format, actualData))
        return dataToBeReturned


    def __getNorthAndGravityVectorsInSensorFrame(self, sensorId):
        command = Commands.getCommandAsChr(Commands.GET_NORTH_AND_GRAVITY_VECTORS_IN_SENSOR_FRAME)
        lengthOfReturnData = Commands.getReturnDataLength(Commands.GET_NORTH_AND_GRAVITY_VECTORS_IN_SENSOR_FRAME)
        format = Commands.getRetrunDataFormat(Commands.GET_NORTH_AND_GRAVITY_VECTORS_IN_SENSOR_FRAME)

        binaryCommand = self.__getWirelessBinaryCommand(command, sensorId)
        receivedData = self.__getRawDataAndRetryIfGetCommandFailed(sensorId,binaryCommand,lengthOfReturnData)
        return (self.__getFormatedData(receivedData,format))


    def __getRawDataAndRetryIfGetCommandFailed(self,sensorId,binaryCommand, returnDataLength):
        WIRELESS_HEADER_LENGTH = 3
        SUCESSFULLY_SENT_BYTE = chr(0x00)
        TOTAL_PACKET_LENGTH = WIRELESS_HEADER_LENGTH + returnDataLength

        self.__sendDataToSerialPort(binaryCommand)
        receivedData = (self.serialLink.readData(TOTAL_PACKET_LENGTH))

        while receivedData[0] != SUCESSFULLY_SENT_BYTE and receivedData[1] != sensorId and receivedData != returnDataLength:
            print "send to sensor Id" + str(sensorId) + "fail"
            self.serialLink.flushBuffer()
            self.__sendDataToSerialPort(binaryCommand)
            receivedData = (self.serialLink.readData(TOTAL_PACKET_LENGTH))
        return receivedData

    def __getFormatedData(self, data, format):
        actualData = data[3:len(data)]
        sensorId = data[1]
        dataToBeReturned = list(struct.unpack(format, actualData))
        dataToBeReturned.insert(0,ord(sensorId))
        return dataToBeReturned

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
            #print ("command successful" + repr(receivedData))
            return True
        else:
            #print ("command failed" + repr(receivedData))
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
