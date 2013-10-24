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
                [0]*dimension]*dimension]*dimension, dtype='bool')
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
        Device.redraw(self)
        if self.emulator:
            wf.setVisible(emulator.findIndexArray(self.array))
            pv.run()

if __name__ == "__main__":
    cube = Cube("", emulator=True)
    pv = emulator.ProjectionViewer(640,480)
    wf = wireframe.Wireframe()
    pv.createCube(wf)
    count = 0;
    start = (0, 0, 0)
    point = (0,0)
    while True:
	
	#planeBounce(cube,(count/20)%2+1,count%20)
	#start = wireframeExpandContract(cube,start)
	#rain(cube,count)
	#time.sleep(.1)
        #point = voxel(cube,count,point)
	sine_wave(cube,count)
	cube.redraw()
	time.sleep(.1)
        count += 1

