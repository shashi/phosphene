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

# this function is passed to audio.playAndRun to be run as
# often as required and possible.
# i is approximately the sample number currently being played
# delta is the number of samples since the previous call to loop
def loop(i, delta):
    if delta > 0:
        fps = sF / delta
        print 'fps:', fps
        sff = getSFFT(data, i, 0.04 * sF)
        bins = bin(11, sff, [0, 25, 50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 22100])
        surface.fill((0,0,0))
        barGraph(surface, (20, 40, 600, 400), bins)
        display.update()

# pass the Sound object and loop function, set update frequency to 90Hz
audio.playAndRun(soundObj, loop, 90)
