import serial
import numpy
import math
import device

# A class for the cube
class Cube(device.Device):
    def __init__(self, port, dimension=10, emulator=False):
        super.__init__(self, "Cube", port)
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
