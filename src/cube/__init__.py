# A class for the cube
import serial
import numpy
import math
import emulator
import mywireframe as wireframe

class Cube:
    def __init__(self, port, dimension=10, emulator=False):
        self.array = numpy.array([[\
                [0]*dimension]*dimension]*dimension, dtype='bool')
        self.dimension = dimension
        self.emulator = emulator

        try:
            self.port = serial.Serial(port)
            self.isConnected = True
        except e:
            self.isConnected = False
            print e

    def set_led(self, x, y, z, level=1):
        self.array[x][y][z] = level

    def get_led(self, x, y, z):
        return self.array[x][y][z]


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
		pv = ProjectionViewer(640,480)
		cube = wireframe.Wireframe()
		pv.createCube(cube)
		visible = []
		for x in range(0,10):
			for y in range(0,10):
				for z in range(0,10):
					if(getled[x][y][z]==1):
						visible.append((x,y,z))
		cube.setVisible(findIndex(visible))
						 

cube = Cube()
