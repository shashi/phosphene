# An example showing how to use the audio module
import serial
import sys
import pygame
from pygame import display
from pygame.draw import *
import scipy

import audio
from signalutil import *
from graphs import *

if len(sys.argv) < 2:
    print "Usage: %s file.mp3" % sys.argv[0]
    sys.exit(1)
else:
    fPath = sys.argv[1]

# Open a pygame display, required for showing the rectangles
pygame.init()
surface = display.set_mode((640, 480))

# read audio data into a numpy array, sF is the sampling frequency
sF, data = audio.read(fPath)
# soundObj is a pygame.mixer.Sound object
soundObj = audio.makeSound(sF, data)

averaged = (data[:, 0] + data[:, 1]) / 2

# this function is passed to audio.playAndRun to be run as
# often as required and possible.
# i is approximately the sample number currently being played
# delta is the number of samples since the previous call to loop
N = 2048
envelope = envelopeVector(N)
equalize = equalizeVector(N)
charize = lambda xs: [chr(x) for x in xs]

State = lambda x: x
State.top = 255
port = serial.Serial("/dev/ttyACM0")


def loop(i, fps):
    if fps > 0:
        print 'fps:', fps
        surface.fill((0,0,0))
        spectrum = getSFFT(averaged, i, N, envelope)
        if len(spectrum) == N/2:
            spectrum = spectrum * equalize
        binsHamLin = group(14, spectrum)
        State.top = State.top * 0.95 + max(binsHamLin[:-8]) * 0.05
        waterFallInput = [min(255, int(k /State.top * 280)) for k in binsHamLin[:-8]]
        print waterFallInput
        try:
            port.write(charize(waterFallInput))
            #print "Got back", [ord(c) for c in port.read(size=9)]
        except e:
            port.close()

        barGraph(surface, (20, 20, 600, 440), waterFallInput)
        binsHamLin = group(32, spectrum)
        #circleRays(surface, (480,240), binsHamLin)
        display.update()

# pass the Sound object and loop function, set update frequency to 90Hz
audio.playAndRun(soundObj, loop, 30)
