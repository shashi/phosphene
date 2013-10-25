import device
from phosphene.signal import *
import scipy, numpy
from phosphene.graphs import barGraph

class Waterfall(device.Device):
    def __init__(self, port):
        device.Device.__init__(self, "Waterfall", port)

    def setupSignal(self, signal):
        def waterfall(s):
            lights = [s.avg8[i] * 200 / max(0.5, s.longavg8[i]) \
                            for i in range(0, 8)]

            fans = [2*i for i in lights]
            lights.reverse()
            return lights + fans

        signal.waterfall = lift(waterfall)

    def graphOutput(self, signal):
        return barGraph(self.truncate(signal.waterfall) / 255.0)

    def redraw(self, signal):
        payload = self.toByteStream(signal.waterfall)
        self.port.write(payload)
