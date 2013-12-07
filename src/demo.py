import sys
import pdb
import pygame
from pygame import display
from pygame.draw import *
import scipy
import time

from phosphene import audio, util, signalutil, signal
from phosphene.graphs import barGraph, boopGraph, graphsGraphs

from threading import Thread

if len(sys.argv) < 2:
    print "Usage: %s file.mp3" % sys.argv[0]
    sys.exit(1)
else:
    fPath = sys.argv[1]

# initialize PyGame
SCREEN_DIMENSIONS = (640, 480)
pygame.init()
surface = display.set_mode(SCREEN_DIMENSIONS)

sF, data = audio.read(fPath)

sig = signal.Signal(data, sF)
sig.A = signal.lift((data[:,0] + data[:,1]) / 2, True)

def beats(s):
    """ Extract beats in the signal in 4 different
        frequency ranges """

    # quick note: s.avg4 is a decaying 4 channel fft
    #             s.longavg4 decays at a slower rate
    # beat detection huristic:
    #       beat occured if s.avg4 * threshold > s.longavg4

    threshold = 1.7
    return util.numpymap(
            lambda (x, y): 1 if x > threshold * y else 0,
            zip(s.avg4 * threshold, s.longavg4))

# Lift the beats
sig.beats = signal.lift(beats)
# not sure if this can be called sustain.
# blend gives a decay effect
sig.sustain = signalutil.blend(beats, 0.7)

def graphsProcess(s):
    # clear screen
    surface.fill((0, 0, 0))
    # draw a decaying fft differential and the beats in the full
    # pygame window.
    graphsGraphs([
        barGraph(s.avg12rel / 10),
        boopGraph(s.beats),
        boopGraph(s.sustain)
    ])(surface, (0, 0) + SCREEN_DIMENSIONS)
    # affect the window
    display.update()

def repl():
    """ call this function to give you a pdb shell
        while the program is running. You will be
        dropped in the current context. """

    def replFunc():
        pdb.set_trace()

    replThread = Thread(target=replFunc)
    replThread.start()
#repl()

# apply utility "lift"s -- this sets up signal.avgN and longavgN variables
signalutil.setup(sig)
soundObj = audio.makeSound(sF, data)
    # make a pygame Sound object from the data
soundObj.play()                      # start playing it. This is non-blocking
# perceive signal at 90 fps (or lesser when not possible)
signal.perceive([graphsProcess], sig, 90)
