#
# This script plays an mp3 file and communicates via serial.Serial
# with devices in the Technites psychedelic room to visualize the
# music on them.
#
# It talks to 4 devices
#   WaterFall -- tubes with LEDs and flying stuff fanned to music
#   DiscoBall -- 8 60 watt bulbs wrapped in colored paper
#   LEDWall   -- a 4 channel strip of LED
#                this time it was the LED roof instead :p
#   LEDCube   -- a 10x10x10 LED cube - work on this is still on
#
# the script also has a sloppy pygame visualization of the fft and
# beats data
#

import sys
import time
import scipy
import pygame
from pygame import display
from pygame.draw import *

import pathsetup # this module sets up PYTHONPATH for all this to work

from devices.discoball import DiscoBall
from devices.waterfall import Waterfall
from devices.ledwall import LEDWall
from devices.cube import Cube

import phosphene
from phosphene import audio, signalutil, util
from phosphene.util import *
from phosphene.signal import *
from phosphene.dsp import *
from phosphene.graphs import *
from phosphene.signalutil import *
from cube import cubeProcess

#from phosphene import cube
from threading import Thread


# Setup devices with their corresponding device files
devs = [
        Waterfall("/dev/ttyACM0"),
        DiscoBall("/dev/ttyACM1"),
        LEDWall("/dev/ttyACM2")
        ]

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



for d in devs:
    d.setupSignal(signal)

def devices(s):
    #threads = []
    for d in devs:
        if d.isConnected:
            def f():
                d.redraw(s)
                d.readAck()
            #t = Thread(target=f)
            #threads.append(t)
            #t.start()
            f()

    #for t in threads:
    #    t.join(timeout=2)
    #    if t.isAlive():
    #        d.isUnresponsive()

    surface.fill((0, 0, 0))
    graphsGraphs(filter(
        lambda g: g is not None,
        [d.graphOutput(signal) for d in devs]))(surface, (0, 0, 640, 480))

CubeState = lambda: 0
CubeState.count = 0

#cube = Cube("/dev/ttyACM1", emulator=True)
def cubeUpdate(signal):
    CubeState.count = cubeProcess(cube, signal, CubeState.count)

def graphsProcess(s):
    display.update()

processes = [graphsProcess, devices] #, cube.emulator]

signal.relthresh = 1.66

soundObj = audio.makeSound(sF, data)
    # make a pygame Sound object from the data

# run setup on the signal
signalutil.setup(signal)
soundObj.play()                      # start playing it. This is non-blocking
perceive(processes, signal, 90)      # perceive your signal.
