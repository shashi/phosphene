# Functions to help you lift and fold
from .signal import *
import numpy
import pdb

def maxDecaying(groups, quantity, rate=0.005):
    return expAvg(lambda sig: max(group(groups, quantity(sig))), rate)

def setup(signal):
    #N = 2048

    ## FFT
    #S.fft = lift(lambda s: fft(s.A[-N/4:3*N/4], envelope(N), equalize(N)))

    ## Differential of the FFT
    #S.flux = foldp( \
    #        lambda s, prev: \
    #            (numpymap(lambda v: max(0, v), s.fft - prev[1]), s.fft), 0)
    #S.y1 = lift(lambda s: s.fft + s.flux)

    ## FFT with exponential averaging
    #S.fftDecaying = expAvg(lambda sig: sig.fft, 0.5)

    ## fft expAvg with a slower rate
    #S.fftDecayingSlowly = expAvg(lambda sig: sig.fft, 0.1)

    ## fft expAvg with a slower rate
    #S.fftContour = expAvg(lambda sig: sig.waterfallFans, 0.0001)

    #S.fftContour7 = lift(lambda s: [pow(s.waterfallFans[i], s.y2[i]) for i in range(0, 7)])

    ## fft differential, expAvged
    #S.fluxDecaying = expAvg(lambda sig: sig.flux, 0.001)
    #signal.fft = lift(lambd s: s
    #S.fftMaxDecaying7 = maxDecaying(7, lambda s: s.fft, 0.005)
    #S.fluxMaxDecaying7 = maxDecaying(7, lambda s: s.flux, rate=0.0005)
    #S.fftMaxDecayingSlowly7 = maxDecaying(7, lambda s: s.fft, rate=0.005)
    #S.y0 = expAvg(lambda sig: sig.fft, 0.0001)
    #S.y1 = maxDecaying(7, lambda s: s.fft, rate=0.005)
    #S.y2 = lift(lambda s: group(7, s.y0) /  s.y1)

    ## Finally, waterfall is just fftDecaying at 0.1
    #S.waterfallFans = lift(lambda s: group(7, s.fftDecayingSlowly) / s.fftMaxDecayingSlowly7)

    ## flux thingy
    #S.fluxThingy = lift(lambda s: group(7, s.fluxDecaying) / s.fluxMaxDecaying7)


def expAvg(f, ratio=lambda s: 0.5):
    """Create the exponential averaging of a signal attribute"""
    # ratio = (lambda s: ratio) if isinstance(ratio, float) else ratio

    g = (lambda s: getattr(s, f)) if isinstance(f, str) else f
    h = (lambda s: ratio) if isinstance(ratio, float) else ratio

    return foldp(lambda s, prev: (g(s) * h(s) + \
            prev[1] * (1-h(s)), prev[0]), 0)

def differential(f):
    S.flux = foldp( \
            lambda s, prev: \
            (f(s), f(s) - prev[1], s.fft), 0)
