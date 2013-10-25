import device
from phosphene.signal import *
from phosphene.graphs import *

class LEDWall(device.Device):
    def __init__(self, port):
        device.Device.__init__(self, "LEDWall", port)

    def setupSignal(self, signal):
        signal.ledwall = lift(lambda s: \
                s.discoball[:6])

    def graphOutput(self, signal):
        return None

    def redraw(self, signal):
        print "LEDWall", self.toByteStream(signal.discoball[:6])
        self.port.write(self.toByteStream(signal.discoball[:6]))
