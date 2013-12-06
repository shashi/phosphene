import serial
import numpy
import math
from device import Device
from cubelib import emulator
from cubelib import mywireframe as wireframe
from animations import *
import time
import threading

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

    def redraw(self, wf=None, pv=None):
        if self.emulator:
            wf.setVisible(emulator.findIndexArray(self.array))
            pv.run()

if __name__ == "__main__":
    cube = Cube("/dev/ttyACM0")
    #pv = emulator.ProjectionViewer(640,480)
    #wf = wireframe.Wireframe()
    #pv.createCube(wf)
    count = 0
    start = (0, 0, 0)
    point = (0,0)
    #fillCube(cube,0)
    #cube.redraw()
    #time.sleep(100)
    def sendingThread():
        while True:
            cube.port.write("S")
            bs = cube.toByteStream()
            for i in range(0, 130):
                time.sleep(0.01)
                cube.port.write(chr(bs[i]))
                print "wrote", bs[i]
            assert(cube.port.read() == '.')

    t = threading.Thread(target=sendingThread)
    t.start()
    #fillCube(cube,0)
    #cube.set_led(9,9,9)
    #for x in range(0, 9):
    #    for y in range(0, 9):
    #        for z in range(0, 9):
    #            cube.set_led(x, y, z, 1)
    #            time.sleep(1)
    while True:
        #wireframeCube(cube,(1,1,1),(9,9,9))
        fillCube(cube, 1)
        #planeBounce(cube,(count/20)%2+1,count%20)
        #planeBounce(cube,1,count)
        #start = wireframeExpandContract(cube,start)
        #rain(cube,count,5,10)
	    #time.sleep(.1)
        #point = voxel(cube,count,point)
	    #sine_wave(cube,count)
	    #pyramids(cube,count)
	    #side_waves(cube,count)
	    #fireworks(cube,4)
        #technites(cube, count)
        #setPlane(cube,1,(counter/100)%10,1)
        #setPlane(cube,2,0,1)
	    #stringPrint(cube,'TECHNITES',count)
        #moveFaces(cube)
        #cube.set_led(0,0,0)
        #cube.set_led(0,0,1)
        cube.redraw()
        count += 1
        time.sleep(0.1)

