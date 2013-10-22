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


try:
    p = serial.Serial("/dev/ttyACM0")
    NOWATERFALL = False
except:
    NOWATERFALL = True

def sendWaterfall(data):
    if NOWATERFALL: return
    bs = bytes(data)
    try:
        p.write(bs)
        # Assuming the thing gives only one char
        p.read(size=1)
    except:
        p.close()

    display.update()

def graphsProcess(s):
    surface.fill((0, 0, 0))
    graphsGraphs(surface, s.graphs)((0, 0, 640, 480))
    display.update()
    print s.fps

processes = [graphsProcess] #, cube.emulator]

S = Signal(data, sF)

S.A = lift((data[:,0] + data[:,1]) / 2, True)

N = 2048

# FFT
S.fft = lift(lambda s: fft(s.A[-N/4:3*N/4], envelope(N), equalize(N)))

# Differential of the FFT
S.flux = foldp( \
        lambda s, prev: \
            (numpymap(lambda v: max(0, v), s.fft - prev[1]), s.fft), 0)
S.y1 = lift(lambda s: s.fft + s.flux)

# FFT with exponential averaging
S.fftDecaying = expAvg(lambda sig: sig.fft, 0.5)

# fft expAvg with a slower rate
S.fftDecayingSlowly = expAvg(lambda sig: sig.fft, 0.1)

# fft expAvg with a slower rate
S.fftContour = expAvg(lambda sig: sig.waterfallFans, 0.0001)

S.fftContour7 = lift(lambda s: [pow(s.waterfallFans[i], s.y2[i]) for i in range(0, 7)])

# fft differential, expAvged
S.fluxDecaying = expAvg(lambda sig: sig.flux, 0.001)

# Keep a decaying maximum value of the decaying thingies
def maxDecaying(groups, quantity, rate=0.005):
    return expAvg(lambda sig: max(group(groups, quantity(sig))), rate)

S.fftMaxDecaying7 = maxDecaying(7, lambda s: s.fft, 0.005)
S.fluxMaxDecaying7 = maxDecaying(7, lambda s: s.flux, rate=0.0005)
S.fftMaxDecayingSlowly7 = maxDecaying(7, lambda s: s.fft, rate=0.005)
S.y0 = expAvg(lambda sig: sig.fft, 0.0001)
S.y1 = maxDecaying(7, lambda s: s.fft, rate=0.005)
S.y2 = lift(lambda s: group(7, s.y0) /  s.y1)

# Finally, waterfall is just fftDecaying at 0.1
S.waterfallFans = lift(lambda s: group(7, s.fftDecayingSlowly) / s.fftMaxDecayingSlowly7)

# flux thingy
S.fluxThingy = lift(lambda s: group(7, s.fluxDecaying) / s.fluxMaxDecaying7)

S.graphs = lift(lambda s: [s.waterfallFans, (0.8 *s.waterfallFans + 0.2 * s.fluxThingy)])
#S.decayFlux = expAvg(lambda sig: sig.flux[0], 0.01)
#S.spectrumIntegral = expAvg(lambda sig: sig.spectrum, 0.01)

soundObj = audio.makeSound(sF, data) # make a pygame Sound object from the data
soundObj.play()                      # start playing it. This is non-blocking
perceive(processes, S, 90)           # perceive your signal.
