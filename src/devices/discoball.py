import device
from phosphene.signal import *
from phosphene.signalutil import *
from phosphene.graphs import *

class DiscoBall(device.Device):
    def __init__(self, port):
        device.Device.__init__(self, "DiscoBall", port)

    def setupSignal(self, signal):
        signal.discoball = lift(lambda s: numpymap(lambda (a, b): 1 if a**2 > b**2 * 2 else 0, zip(s.avg12, s.longavg12)))

    def graphOutput(self, signal):
        return boopGraph(signal.discoball[:4])

    def redraw(self, signal):
        data = self.truncate(signal.discoball[:4] * 255)
        print data
        self.port.write(self.toByteStream(data))
