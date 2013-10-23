# Functions to help you lift and fold
from .signal import *
from dsp import *
import numpy
import pdb

def maxDecaying(groups, quantity, rate=0.005):
    return expAvg(lambda sig: max(group(groups, quantity(sig))), rate)

def setup(signal, horizon=2048):

    signal.spectrum = lift(lambda s: \
            fft(s.A[-horizon/2:horizon/2], 32, True, True))

    signal.spectralFlux = foldp(lambda s, prev: \
            (numpymap(lambda v: max(0, v), s.spectrum - prev[1]), s.spectrum), 0)


def expAvg(f, ratio=lambda s: 0.5):
    """Create the exponential averaging of a signal attribute"""
    # ratio = (lambda s: ratio) if isinstance(ratio, float) else ratio

    g = (lambda s: getattr(s, f)) if isinstance(f, str) else f
    h = (lambda s: ratio) if isinstance(ratio, float) else ratio

    return foldp(lambda s, prev: (g(s) * h(s) + \
            prev[1] * (1-h(s)), prev[0]), 0)

def differential(f, nonegatives=False):
    if nonegatives:
        return foldp( \
            lambda s, prev: \
            (numpymap(lambda v: max(0, v), f(s) - prev[1]), f(s)), 0)
    else:
        return foldp( \
            lambda s, prev: \
                (f(s) - prev[1], f(s)), 0)
