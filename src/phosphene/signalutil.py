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

    for i in [1, 3, 4, 5, 6, 8, 12, 16, 32]:
        setup_bands(signal, i)

def setup_bands(signal, bands):

    def get(s, prefix):
        return getattr(s, prefix + str(bands))

    setattr(signal, 'chan%d' % bands,
            lift(lambda s: group(bands, s.fft)))

    setattr(signal, 'avg%d' % bands,
            blend(lambda s: get(s, 'chan'),
                    lambda s, v, avg: 0.2 if v > avg else 0.5))

    setattr(signal, 'longavg%d' % bands,
            blend(lambda s: get(s, 'chan'),
                    lambda s, v, avg: 0.9 if s.frames < 50 else 0.992))
    # Booya.
    thresh = 1.7
    setattr(signal, 'peaks%d' % bands,
            blend(lambda s: get(s, 'avg') > thresh * get(s, 'longavg'),
                    lambda s, v, a: 0.2))

    setattr(signal, 'chan%drel' % bands,
            lift(lambda s: numpymap(
                lambda (x, y): x / y if y > 0.001 else 1,
                    zip(get(s, 'chan'), get(s, 'longavg')))))

    setattr(signal, 'avg%drel' % bands,
            lift(lambda s: numpymap(
                lambda (x, y): x / y if y > 0.001 else 1,
                    zip(get(s, 'avg'), get(s, 'longavg')))))
    ## Detecting beats

def normalize(data, signal, divisor=None):
    if divisor is None: divisor = lambda s, n: getattr(s, 'longavg%d' % n)
    n = len(data)
    divs = divisor(signal, n)
    return numpymap(lambda (a, b): a / max(0.01, b), zip(data, divs))

def fallingMax(f, minf=lambda s: 0.5, cutoff=0.95, gravity=lambda s: 0.9):
    def maxer(signal, prev):
        # prev contains:
        thisFrame = f(signal)

        if prev == None:
            init = (thisFrame, [signal.t] * len(thisFrame))
            return (init, init)

        maxVal, maxTime = prev
        mins = minf(signal)
        try:
            s = sum(mins)
        except:
            s = mins

        for i in range(0, len(thisFrame)):
            if thisFrame[i] > cutoff * maxVal[i] and s != 0:
                # Update
                maxVal[i] = thisFrame[i]
                maxTime[i] = signal.t
            else:
                # Fall
                maxVal[i] -= gravity(signal) * (signal.t - maxTime[i])
        return ((maxVal, maxTime), (maxVal, maxTime))
    return foldp(maxer, None)

def boopValue(t2, maxes):
    maxVal, maxTime = maxes
    return numpy.array([math.exp(-(t2 - t1) * 9) for t1 in maxTime])

def blend(f, rate=lambda s, val, avg: 0.3):
    def blender(signal, avg):
        vals = f(signal)
        l = len(vals)

        # None is the starting value
        if avg is None: avg = [0] * l

        for i in range(0, l):
            if isinstance(rate, float):
                r = rate
            elif hasattr(rate, '__call__'):
                r = rate(signal, vals[i], avg[i])
            else:
                ValueError("rate of decay must be a float or a lambda")
            r = adjustRate(r, signal) # adjust based on fps
            avg[i] = avg[i] * r + vals[i] * (1-r)
        avg = numpy.array(avg)
        return (avg, avg)       # required by foldp
    return foldp(blender, None)

def adjustRate(r, signal):
    # THANKS MILKDROP! FOR EVERYTHING!
    pow = math.pow
    return pow(pow(r, signal.max_fps), 1.0/signal.fps)
