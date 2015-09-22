__author__ = 'aknay'
import ListOfCommands

from CommandCenter import CommandCenter

commandCenter = CommandCenter("/dev/ttyACM0")
print (commandCenter.getTaredOrientationAsQuaternion(sensorId=1))



#commandCenter.startStreaming(sensorId=2)

#commandCenter.stopStreaming(sensorId=2)
print (commandCenter.getStreamingTiming(sensorId=1))
commandCenter.setStreamingTiming(interval=0, druation=10000, delay=0, sensorId=1)

#commandCenter.test()

#print (commandCenter.getStreamingTiming(sensorId=1))
