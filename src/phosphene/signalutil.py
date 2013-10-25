# Functions to help you lift and fold
from .signal import *
from dsp import *
import numpy
import pdb
import math

def setup(signal, horizon=576):
    # Note of awesome: this only sets up dependencies,
    # things absolutely necessary are evaluated.

    signal.fft = lift(lambda s: \
            fft(s.A[-horizon/2:horizon/2], False, True, True))

    for i in [3, 4, 5, 6, 8, 12, 16, 32]:
        setupBands(signal, i)

def setupBands(signal, bands):
    get = lambda s, prefix: getattr(s, prefix + str(bands))

    setattr(signal, 'chan%d' % bands,
            lift(lambda s: group(bands, s.fft))) # creates chan3, chan6..chan32
    setattr(signal, 'avg%d' % bands,
            blend(lambda s: get(s, 'chan'),
                    lambda s, v, avg: 0.2 if v > avg else 0.5))
    setattr(signal, 'longavg%d' % bands,
            blend(lambda s: get(s, 'chan'),
                    lambda s, v, avg: 0.9 if s.frames < 50 else 0.992))
    # Booya.
    setattr(signal, 'peaks%d' % bands,
            blend(lambda s: get(s, 'chan') > 1.5 * get(s, 'avg'),
                    lambda s, v, a: 0.2))
    setattr(signal, 'chan%drel' % bands,
            lift(lambda s: numpymap(lambda (x, y): x / y if y > 0.001 else 1, \
                    zip(get(s, 'chan'), get(s, 'longavg')))))
    setattr(signal, 'avg%drel' % bands,
            lift(lambda s: numpymap(lambda (x, y): x / y if y > 0.001 else 1, \
                    zip(get(s, 'avg'), get(s, 'longavg')))))
    ## Detecting beats


def fallingMax(f, minf=lambda s: 0.5, thresh=0.9, gravity=lambda s: 0.5):
    def maxer(signal, prev):
        thisFrame = f(signal)
        minFrame = minf(signal)
        
        for i in range(0, len(thisFrame)):
            if thisFrame[i] > 0.9 * prevFrame[i]: pass
                

def blend(f, rate=lambda s, val, avg: 0.3):
    def blender(signal, avg):
        vals = f(signal)
        l = len(vals)

        # see foldp for why.
        if avg[1] is None: avg = [0] * l
        else: avg = avg[1]

        for i in range(0, l):
            r = rate(signal, vals[i], avg[i])
            r = adjustRate(r, signal) # adjust based on fps
            avg[i] = avg[i] * r + vals[i] * (1-r)
        avg = numpy.array(avg)
        return (avg, avg)       # required by foldp
    return foldp(blender, None)

def adjustRate(r, signal):
    # THANKS MILKDROP! FOR EVERYTHING!
    pow = math.pow
    return pow(pow(r, signal.prefFps), 1.0/signal.fps)
