import sys
import pdb
import pygame
from pygame import display
from pygame.draw import *
import scipy
import time

import devices
from devices.discoball import DiscoBall
from devices.waterfall import Waterfall
from devices.ledwall import LEDWall

import phosphene
from phosphene import audio
from phosphene.util import *
from phosphene.signal import *
from phosphene.dsp import *
from phosphene.graphs import *
from phosphene.signalutil import *

#from phosphene import cube
from threading import Thread

import os, sys
if os.environ.has_key('PYTHONPATH'):
    os.environ['PYTHONPATH'] += os.pathsep + os.path.dirname(__file__)
else:
    os.environ['PYTHONPATH'] = os.path.dirname(__file__)

pygame.init()
surface = display.set_mode((640, 480))

if len(sys.argv) < 2:
    print "Usage: %s file.mp3" % sys.argv[0]
    sys.exit(1)
else:
    fPath = sys.argv[1]

sF, data = audio.read(fPath)

import serial

signal = Signal(data, sF)

signal.A = lift((data[:,0] + data[:,1]) / 2, True)

signal.fallingMax = fallingMax(lambda s: s.avg4rel, lambda s: s.longavg4)

def graphsProcess(s):
    surface.fill((0, 0, 0))
    boops = boopValue(s.t, s.fallingMax)
    boops[3] = boops[0]
    graphsGraphs([barGraph(s.avg4rel), boopGraph(boops)])(surface, (0, 0, 640, 480))
    display.update()

processes = [graphsProcess]

# run setup on the signal
setup(signal)

soundObj = audio.makeSound(sF, data)
    # make a pygame Sound object from the data

def repl():

    def replFunc():
        pdb.set_trace()

    replThread = Thread(target=replFunc)
    replThread.start()

repl()

soundObj.play()                      # start playing it. This is non-blocking
perceive(processes, signal, 90)      # perceive your signal.
