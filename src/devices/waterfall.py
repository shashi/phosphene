import device
from phosphene.signal import *

def reverse(lst):
    new = [i for i in lst]
    new.reverse()
    return new

class Waterfall(device.Device):
    def __init__(self, port):
        device.Device.__init__(self, "Waterfall", port)

    def setupSignal(self, signal):
        signal.waterfall = lift(lambda s: \
                [s.avg8[i] / 50 for i in range(0,8)])

    def graphOutput(self, signal):
        return reverse(signal.waterfall) + [3*i for i in signal.waterfall]

    def redraw(self, signal):
        payload = self.toByteStream()
        print payload
        self.port.write(payload)
