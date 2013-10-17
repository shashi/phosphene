# An example showing how to use the audio module

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
N = 1024
PI = 6.2831853 / 2
mult = PI / N
power = 1
envelope = numpy.array([pow(0.5 + 0.5 * scipy.sin(i*mult - 1.5707963268), power) for i in range(0, N)])
N_2 = N / 2
equalize = numpy.array([-0.04 * scipy.log((N_2-i) * 1.0/N_2) for i in range(0, N_2)])

def loop(i, fps):
    if fps > 0:
        print 'fps:', fps
        surface.fill((0,0,0))
        spectrum = getSFFT(averaged, i, 1024, envelope)
        if len(spectrum) == 512:
            spectrum = spectrum * equalize
        binsHamLin = bin(128, spectrum)
        barGraph(surface, (20, 20, 600, 440), binsHamLin, lambda v: abs(v) / 300)
        display.update()

# pass the Sound object and loop function, set update frequency to 90Hz
audio.playAndRun(soundObj, loop, 90)
