__author__ = 'aknay'
import serial


class SerialPort:
    def __init__(self, port):
        self.serialPort = serial.Serial(port, timeout=0.1, writeTimeout=0.1, baudrate=115200)

    def sendData(self, data):
        self.serialPort.write(data)

    def readData(self, size):
        return self.serialPort.read(size)

    def clostPort(self):
        self.serialPort.close()

    def flushBuffer(self):
        self.serialPort.flushInput()
        self.serialPort.flushOutput()
        self.serialPort.flush()

    def getNumberOfByteAvailable(self):
        return self.serialPort.inWaiting()


