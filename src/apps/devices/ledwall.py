import device
from phosphene.signal import *
from phosphene.signalutil import *
from phosphene.graphs import *

class LEDWall(device.Device):
    def __init__(self, port):
        device.Device.__init__(self, "LEDWall", port)

    def setupSignal(self, signal):
        CHANNELS = 6 
        val = lambda s: [max(0, scipy.log(s.avg3[0]+1)) - scipy.log(s.longavg3[0]+1)]
        signal.avg1Falling = fallingMax(val)
        def f(s):
            n = int(min(6, max(0, val(s)[0] * CHANNELS / (s.avg1Falling[0] if s.avg1Falling[0] > 0.01 else 1))))
            return [1 for i in range(0, n)] + [0 for i in range(0, 6-n)]
        signal.ledwall = lift(f)

    def graphOutput(self, signal):
        return None

    def redraw(self, signal):
        print "LEDWall", self.toByteStream(signal.ledwall)
        self.port.write(self.toByteStream(signal.ledwall))
