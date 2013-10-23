class Device:
    def __init__(self, name, port):
        self.name = name
        self.array = []
        try:
            self.port = serial.Serial(port)
            self.isConnected = True
        except Exception:
            self.port = None
            self.isConnected = False

    def takeSignal(self, signal):
        pass

    def setupSignal(self, signal):
        pass

    def toByteStream(self):
        return ''

    def redraw(self):
        if self.isConnected:
            self.port.write(self.toByteStream())
            self.port.read(size=1) #Acknowledgement
        else:
            print "Connection to %s lost!" % self.name

