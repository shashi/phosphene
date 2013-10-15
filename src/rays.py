# An example showing how to use the audio module

import sys
import pygame
from pygame import display
from pygame.draw import *

import audio
from signalutil import *

if len(sys.argv) < 2:
    print "Usage: %s file.mp3" % sys.argv[0]
    sys.exit(1)
else:
    fPath = sys.argv[1]

# Open a pygame display, required for showing the lines
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
def loop(i, fps):
    if fps > 0:
        print 'fps:', fps
        surface.fill((0,0,0))
        spectrum = getSFFT(averaged, i, 1024)
        binsHamLin = bin(64, spectrum)
        circlerays(surface, (160,240), binsHamLin)
        sff = getSFFT(averaged, i, 1024, lambda n: 1) # no window
        binsRectLin = bin(64, sff)
        circlerays(surface, (480,240), binsRectLin)
        display.update()

# pass the Sound object and loop function, set update frequency to 90Hz
audio.playAndRun(soundObj, loop, 90)
