import device
from phosphene.signal import *

class LEDWall(device.Device):
    def __init__(self, port):
        device.Device.__init__(self, "LEDWall", port)

    def setupSignal(self, signal):
        signal.ledwall = lift(lambda s: \
                [s.avg8[i]/ 40 for i in range(0,8)])

    def graphOutput(self, signal):
        return signal.discoball[:4]

    def redraw(self, signal):
        print "LEDWall", self.toByteStream(signal.ledwall[:-2])
        self.port.write(self.toByteStream(signal.ledwall[:-2]))
