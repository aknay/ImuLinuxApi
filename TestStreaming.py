__author__ = 'aknay'


##############################################################################################
#Author = aknay
#Note:
#
#
##############################################################################################
import threading
import Queue
import math
import Commands
from CommandCenter import CommandCenter
from VectorAndQuaternionCalculator import VectorAndQuaternionCalculator


from time import sleep


class Producer(threading.Thread):
    """
    Produces random integers to a list
    """
    def __init__(self, queue):
        """
        Constructor.

        @param integers list of integers
        @param queue queue synchronization object
        """
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):

        commandCenter = CommandCenter("/dev/ttyACM0")

        #need to be in T position
        #buttons are facing up and the LEDs are pointed towards the shoulder


        '''



        offsetOfSensorOne = commandCenter.performOffsetOperation(sensorId=1)
        #closet to chr(0x0B) gravity = [0,-1,0] and suppliedVector =  [0,0,1]

        #offsetOfSensorTwo = commandCenter.performOffsetOperation(sensorId=2)

        sleep(1)

        while (1):

            forwardVectorOfSensorOne = commandCenter.getDeviceVector(sensorId=1,suppliedVector= [0.0,1.0,0.0],offsetAsQuaternion=offsetOfSensorOne)

            print "forwardVectorOne %s" % (forwardVectorOfSensorOne)
            #print"Radians: %0.4f\tDegrees: %0.4f" % (angle, math.degrees(angle))
            #print forwardVectorOfSensorOne

            #forwardVectorOfSensorTwo = commandCenter.getDeviceVector(sensorId=2,suppliedVector= [0.0,0.0,1.0],offsetAsQuaternion=offsetOfSensorTwo)

            #print "forwardVectorTwo"
            #print forwardVectorOfSensorTwo

            #upVector = commandCenter.getDeviceVector(sensorId=1,suppliedVector= [0.0,1.0,0.0], offsetAsQuaternion=offsetOfSensorOne)

            #print "upVector"
            #print upVector


            sleep(2)




        '''



        offsetOfSensorOne = commandCenter.performOffsetOperation(sensorId=1)
        offsetOfSensorTwo = commandCenter.performOffsetOperation(sensorId=2)

        print "offsetOfSensorOne"
        print offsetOfSensorOne

        print "offsetOfSensorTwo"
        print offsetOfSensorTwo


        while (1):



            '''
            forwardVectorOfSensorOne = commandCenter.getDeviceVector(sensorId=1,suppliedVector= [0.0,0.0,1.0],offsetAsQuaternion=offsetOfSensorOne)
            #forwardVectorOfSensorTwo = commandCenter.getDeviceVector(sensorId=2,suppliedVector= [0.0,0.0,1.0],offsetAsQuaternion=offsetOfSensorTwo)
            forwardVectorOfSensorTwo = commandCenter.getDeviceVector(sensorId=2,suppliedVector= [0.0,0.0,-1.0],offsetAsQuaternion=offsetOfSensorTwo)
            print "forwardVectorOne"
            print forwardVectorOfSensorOne

            print "forwardVectorTwo"
            print forwardVectorOfSensorTwo
            # the two sensor rotate around y axis. therefore, x = 0, y = 1 and z = 0
            #not sure; since left hand rotates clockwise, there is downward vector. I think therefore, need to put -1
            upVector = commandCenter.getDeviceVector(sensorId=1,suppliedVector= [0.0,-1.0,0.0], offsetAsQuaternion=offsetOfSensorOne)

            print "upVector"
            angle = commandCenter.getAngleBetweenThreeVectors(forwardVectorOfSensorTwo,forwardVectorOfSensorOne,upVector)

            print "Hinge"
            print"Radians: %0.4f\tDegrees: %0.4f" % (angle, math.degrees(angle))
            sleep(1)
            '''

            #seting z axis as forward vector. rotation about z axis doesn't affect the the vector value.
            #if we rotate about x or y axiss, there will be change in values
            forwardVectorOfSensorOne = commandCenter.getDeviceVector(sensorId=1,suppliedVector= [0.0,0.0,1.0],offsetAsQuaternion=offsetOfSensorOne)
            forwardVectorOfSensorTwo = commandCenter.getDeviceVector(sensorId=2,suppliedVector= [0.0,0.0,-1.0],offsetAsQuaternion=offsetOfSensorTwo)
            print "forwardVectorOne"
            print forwardVectorOfSensorOne

            print "forwardVectorTwo"
            print forwardVectorOfSensorTwo

            # the two sensor rotate around y axis. therefore, x = 0, y = 1 and z = 0
            #not sure; I think it is using LHR. left hand clockwise 1, right hand anti clockwise -1
            upVector = commandCenter.getDeviceVector(sensorId=1,suppliedVector= [0.0,-1.0,0.0], offsetAsQuaternion=offsetOfSensorOne)

            print "upVector"
            angle = commandCenter.getAngleBetweenThreeVectors(forwardVectorOfSensorTwo,forwardVectorOfSensorOne,upVector)

            print "Hinge"
            print"Radians: %0.4f\tDegrees: %0.4f" % (angle, math.degrees(angle))
            sleep(1)







     #   commandCenter.calculateDeviceVector(sensorId=1,vector = [1,0,0],offset=offsetOfSensorOne)




        #commandCenter.stopStreaming(sensorId=2)
        #commandCenter.stopStreaming(sensorId=1)
        #
        # INFINITE_DURATION = 4294967295
        #
        # commandCenter.setStreamingSlot(sensorId=1,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)
        # commandCenter.setStreamingSlot(sensorId=2,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)
        #
        # #100hz, infinite duration, start after 2sec
        # #10000 = 100hz
        # commandCenter.setStreamingTiming(interval=100000,duration=INFINITE_DURATION,delay=3000000,sensorId=1)
        # commandCenter.setStreamingTiming(interval=100000,duration=INFINITE_DURATION,delay=3010000,sensorId=2)
        #
        # commandCenter.startStreaming(sensorId=1)
        # commandCenter.startStreaming(sensorId=2)










        """
        Thread run method. Append random integers to the integers list at
        random time.
        """


        # while True:
        #     packetReceived = commandCenter.getThisData()
        #     if len(packetReceived) == 5:
        #         print packetReceived
        #         self.queue.put(packetReceived)






class Consumer(threading.Thread):
    """
    Consumes random integers from a list
    """

    def __init__(self, queue):
        """
        Constructor.

        @param integers list of integers
        @param queue queue synchronization object
        """
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        """
        Thread run method. Consumes integers from list
        """

        # commandCenter = CommandCenter("/dev/ttyACM0")
        # print (commandCenter.getTaredOrientationAsQuaternion(sensorId=1))



        while True:
            integer = self.queue.get()
            print '%s popped from list by %s' % (integer, self.name)
            self.queue.task_done()






            #time.sleep(0.5)



def main():
    queue = Queue.Queue()
    t1 = Producer(queue)
    t2 = Consumer(queue)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    main()










































'''







commandCenter = CommandCenter("/dev/ttyACM0")


print (commandCenter.getTaredOrientationAsQuaternion(sensorId=1))

INFINITE_DURATION = 4294967295

#just in case if you cant stop
commandCenter.stopStreaming(sensorId=2)
commandCenter.stopStreaming(sensorId=1)




commandCenter.setStreamingSlot(sensorId=1,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)
commandCenter.setStreamingSlot(sensorId=2,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)

commandCenter.setStreamingTiming(10000,INFINITE_DURATION,3000000,sensorId=1)
commandCenter.setStreamingTiming(10000,INFINITE_DURATION,3000000,sensorId=2)


#100hz, infinite duration, start after 2sec
commandCenter.startStreaming(sensorId=1)
commandCenter.startStreaming(sensorId=2)
sleep(4)


commandCenter.getThisData()


# while True:
#     bytesToRead = ser.inWaiting()
#     ser.read(bytesToRead)




#commandCenter.getSerialBuffer()

commandCenter.stopStreaming(sensorId=2)
commandCenter.stopStreaming(sensorId=1)




#commandCenter.getTaredOridntationAsQuaternionFromBuffer(sensorId=1)
commandCenter.getSerialBuffer()

sleep(5)

commandCenter.getTaredOridntationAsQuaternionFromBuffer(sensorId=1)

#commandCenter.closeSerialPort()
'''
'''

commandCenter.setStreamingSlot(sensorId=1,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)
commandCenter.setStreamingSlot(sensorId=2,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)


#100hz, infinite duration, start after 2sec
commandCenter.setStreamingTiming(10000,INFINITE_DURATION,3000000,sensorId=1)

commandCenter.flushBuffer()

#sleep(1)

commandCenter.startStreaming(sensorId=1)
commandCenter.flushBuffer()
#commandCenter.startStreaming(sensorId=2)




sleep(3.5)

commandCenter.stopStreaming(sensorId=1)
#commandCenter.stopStreaming(sensorId=2)

commandCenter.getSerialBuffer()
commandCenter.flushBuffer()

'''




'''

#commandCenter.startStreaming(sensorId=2)

#commandCenter.stopStreaming(sensorId=2)
#print (commandCenter.getStreamingTiming(sensorId=1))
commandCenter.setStreamingSlot(sensorId=1,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)

commandCenter.setStreamingSlot(sensorId=2,slot1=ListOfCommands.SLOT_GET_TARED_QUAT)


commandCenter.startStreaming(sensorId=1)
commandCenter.startStreaming(sensorId=2)

time.sleep(3)

commandCenter.stopStreaming(sensorId=1)
commandCenter.stopStreaming(sensorId=2)

#commandCenter.flushBuffer()

commandCenter.getSerialBuffer()
#commandCenter.closeSerialPort()
'''




#4294967295
#commandCenter.setStreamingTiming(interval=0, duration=4294967295, delay=0, sensorId=1)

#commandCenter.test()

#print (commandCenter.getStreamingTiming(sensorId=1))
#commandCenter.stopStreaming(sensorId=1)