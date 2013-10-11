import pygame
from pygame import display
from pygame.draw import *

import audio
from signalutil import *

# Open a pygame display
pygame.init()
surface = display.set_mode((640, 480))
sF, data = audio.read("/home/shashi/death.mp3")
soundObj = audio.makeSound(sF, data)

def loop(i, delta):
    if delta > 0:
        fps = sF / delta
        print 'fps:', fps
        sff = getSFFT(data, i, 0.04 * sF)
        bins = bin(30, sff, lambda i: i)
        surface.fill((0,0,0))
        barGraph(surface, (20, 40, 600, 400), bins)
        display.update()

audio.playAndRun(soundObj, loop, 90)
