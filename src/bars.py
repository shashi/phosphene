# An example showing how to use the audio package
import pygame
from pygame import display
from pygame.draw import *

import audio
from signalutil import *

# Open a pygame display, required for showing the rectangles
pygame.init()
surface = display.set_mode((640, 480))

# read audio data into a numpy array, sF is the sampling frequency
sF, data = audio.read("/home/shashi/death.mp3")
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
        binsHamLin = spectrum #bin(128, spectrum)
        barGraph(surface, (20, 20, 600, 200), binsHamLin)
        #sff = getSFFT(averaged, i, 1023, lambda n: 1)
        #binsRectLin = bin(128, sff)
        #barGraph(surface, (20, 220, 600, 200), binsRectLin)
        display.update()

# pass the Sound object and loop function, set update frequency to 90Hz
audio.playAndRun(soundObj, loop, 90)
