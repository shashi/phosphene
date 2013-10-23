import serial
import numpy
import math
from device import Device
from cubelib import emulator
from cubelib import mywireframe as wireframe
from animations import *
import time
# A class for the cube
class Cube(Device):
    def __init__(self, port, dimension=10, emulator=False):
        Device.__init__(self, "Cube", port)
        self.array = numpy.array([[\
                [1]*dimension]*dimension]*dimension, dtype='bool')
        self.dimension = dimension
        self.emulator = emulator

    def set_led(self, x, y, z, level=1):
        self.array[x][y][z] = level

    def get_led(self, x, y, z):
        return self.array[x][y][z]

    def takeSignal(self, signal):
        pass

    def toByteStream(self):
        bts = '\x00' * math.ceil((dimension**3) / 8)
        pos = 0
        mod = 0

        for a in self.array:
            for b in a:
                for bit in b:
                    if bit: bts[pos] |= 1 << mod
                    else: bts[pos] &= ~(1 << mod)

                    mod += 1

                    if mod == 8:
                        mod = 0
                        bts += 1
        return bts

    def redraw(self):
	if self.isConnected:
            self.port.write(self.toByteStream())
            self.port.read(size=1) #Acknowledgement		
        else:
                print "Connection to cube lost!"
        if self.emulator:
            wf.setVisible(emulator.findIndexArray(self.array))
            pv.run()

cube = Cube("", emulator=True)
pv = emulator.ProjectionViewer(640,480)
wf = wireframe.Wireframe()
pv.createCube(wf)
count = 1;
while True:
    	planeBounce(cube,1,True)
	cube.redraw()
	count += 2

