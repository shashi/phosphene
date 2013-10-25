import device
from phosphene.signal import *

class DiscoBall(device.Device):
    def __init__(self, port):
        device.Device.__init__(self, "DiscoBall", port)

    def setupSignal(self, signal):
        signal.discoball = lift(lambda s: \
                [s.avg6[i] / 50 for i in range(0,6)])

    def graphOutput(self, signal):
        return signal.discoball[:4]

    def redraw(self, signal):
        data = signal.discoball[:4]
        self.port.write(self.toByteStream(data))
