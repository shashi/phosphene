import serial
import numpy
from threading import Thread

class Device:
    def __init__(self, name, port):
        self.array = []
        try:
            self.port = serial.Serial(port)
            self.isConnected = True
            print "Connected to", name
        except Exception as e:
            self.port = None
            self.isConnected = False
            print "Error connecting to", name, e

    def setupSignal(self, signal):
        pass

    def graphOutput(self, signal):
        pass

    def truncate(self, array):
        return numpy.array([min(int(i), 255) for i in array])

    def toByteStream(self, array):
        return [chr(i) for i in self.truncate(array)]

    def readAck(self):
        print self.port.read(size=1) # Read the acknowledgement

    def redraw(self):
        if self.isConnected:
            self.port.write(self.toByteStream())
            self.port.read(size=1) #Acknowledgement
        else:
            print "Connection to %s lost!" % self.name

    def isUnresponsive(self):
        print "%s is not responding! Stopping to communicate."
        self.isConnected = False

