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

def test_process(s):
    surface.fill((0, 0, 0))
    #barGraph(surface, group(7, s.decayThingy))((0, 0, 640, 480))
    graphsGraphs(surface, s.debug)((0, 0, 640, 480))
    display.update()
    print s.fps

processes = [test_process] #, cube.emulator]

S = Signal(data, sF)

S.A = lift((data[:,0] + data[:,1]) / 2, True)

N = 2048
S.spectrum = lift(lambda s: fft(s.A[-N/4:3*N/4], envelope(N), equalize(N)))
S.flux = foldp(lambda s, prev: \
        (numpymap(lambda v: max(0, v), s.spectrum - prev[1]), \
            s.spectrum), \
        (0, 0))
S.fluxedSpec = lift(lambda s: s.spectrum + 0.1 * s.flux[0])

S.decaySpectrum = expAvg(lambda sig: sig.spectrum, 0.01)
S.decayFlux = expAvg(lambda sig: sig.flux[0], 0.1)
S.decayThingy = lift(lambda sig: sig.decaySpectrum[0] + sig.decayFlux[0])
S.debug = lift(lambda sig: [group(12, (sig.decaySpectrum + sig.decayFlux)[0]), group(12, sig.decayFlux[0])])
S.decayThingyThingy = expAvg(lambda sig: sig.decayThingy[0], 0.01)
S.decayThingyNoKidding = expAvg(lambda sig: (sig.decaySpectrum[0] + sig.decayFlux[0]), lambda sig: max(1.0, group(1, sig.decayThingyThingy[0])[0]/11000))

soundObj = audio.makeSound(sF, data) # make a pygame Sound object from the data
soundObj.play()                      # start playing it. This is non-blocking
perceive(processes, S, 90)           # perceive your signal.
