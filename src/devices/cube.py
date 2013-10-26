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
        self.name = "Cube"

    def set_led(self, x, y, z, level=1):
        self.array[x][y][z] = level

    def get_led(self, x, y, z):
        return self.array[x][y][z]

    def takeSignal(self, signal):
        pass

    def toByteStream(self):
        # 104 bits per layer, first 4 bits waste.
 
        bytesPerLayer = int(math.ceil(self.dimension**2 / 8.0))
        print bytesPerLayer
        discardBits = bytesPerLayer * 8 - self.dimension**2
        print discardBits
        bts = bytearray(bytesPerLayer*self.dimension)

        pos = 0
        mod = 0

        for layer in self.array:
            mod = discardBits
            for row in layer:
                for bit in row:
                    if bit: bts[pos] |= 1 << mod
                    else: bts[pos] &= ~(1 << mod)

                    mod += 1

                    if mod == 8:
                        mod = 0
                        pos += 1
        return bts

    def redraw(self, wf, pv):
        Device.redraw(self)
        if self.emulator:
            wf.setVisible(emulator.findIndexArray(self.array))
            pv.run()

if __name__ == "__main__":
    cube = Cube("/dev/ttyACM0")
    #pv = emulator.ProjectionViewer(640,480)
    #wf = wireframe.Wireframe()
    #pv.createCube(wf)
    count = 0;
    start = (0, 0, 0)
    point = (0,0)
    #fillCube(cube,0)
    #cube.redraw()
    #time.sleep(100)
    while True:
        fillCube(cube,0)
        #planeBounce(cube,(count/20)%2+1,count%20)
        #start = wireframeExpandContract(cube,start)
	    #rain(cube,count,5,10)
	    #time.sleep(.1)
        #point = voxel(cube,count,point)
	    #sine_wave(cube,count)
	    #pyramids(cube,count)
	    #side_waves(cube,count)
	    #fireworks(cube,4)
	    #technites(cube,count)
	    #setPlane(cube,3,0,Z())
	    #stringPrint(cube,'TECHNITES',count)
        #moveFaces(cube)
        cube.redraw()
        time.sleep(.1)
        count += 1
