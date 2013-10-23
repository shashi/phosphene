import device

class Waterfall(device.Device):
    def __init__(self, port):
        super.__init__(self, "Waterfall", port)
    def takeSignal(self, signal):
        
