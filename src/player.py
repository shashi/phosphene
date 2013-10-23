import sys
import pygame
from pygame import display
from pygame.draw import *
import scipy
import time

from phosphene import audio
from phosphene.util import *
from phosphene.signal import *
from phosphene.dsp import *
from phosphene.graphs import *
from phosphene.signalutil import *
#from phosphene import cube

pygame.init()
surface = display.set_mode((640, 480))

if len(sys.argv) < 2:
    print "Usage: %s file.mp3" % sys.argv[0]
    sys.exit(1)
else:
    fPath = sys.argv[1]

sF, data = audio.read(fPath)

import serial

def bytes(d):
    return [chr(min(255, int(d[i] * 255))) for i in range(0, len(d))] 

def graphsProcess(s):
    surface.fill((0, 0, 0))
    graphsGraphs(surface, s.spectrum)((0, 0, 640, 480))
    display.update()
    print s.fps

processes = [graphsProcess] #, cube.emulator]

signal = Signal(data, sF)

signal.A = lift((data[:,0] + data[:,1]) / 2, True)

# run setup on the signal
setup(signal)

soundObj = audio.makeSound(sF, data)
    # make a pygame Sound object from the data
soundObj.play()                      # start playing it. This is non-blocking
perceive(processes, signal, 90)      # perceive your signal.
