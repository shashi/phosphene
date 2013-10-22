import scipy
import numpy
from util import *

def fftIdx(Fs, Hz, n):
    assert(Hz <= Fs / 2);
    return round(Fs / n * Hz)

memFftIdx = memoize(fftIdx)

def getNotes():
    return [0] \
           + [16.35 * pow(2, i/12.0) + 1 for i in range(0, 101)] \
           + [11050, 22100]

def group(n, fft, grouping=lambda i: i):
    """
        Put fft data into n bins by adding them.

        grouping function defines how things are grouped
        lambda i: i       --> linear grouping
        lambda i: 2 ** i  --> logarithmic
    """
    if isinstance(n, (list,tuple)):
        splitPoints = numpy.array(n, dtype=float)
        n = len(n) - 1
    elif hasattr(grouping, '__call__'):
        splitPoints = numpy.array([grouping(i) for i in range(0, n + 1)], \
                dtype=float)
    l = len(fft)

    splitIdx = splitPoints / abs(max(splitPoints)) * l
    splitIdx = [int(i) for i in splitIdx]
    #pdb.set_trace()

    return [sum(fft[splitIdx[i-1]:splitIdx[i]]) for i in range(1, n + 1)]

def fft(samples, envelope=None, equalize=None):
    """
        Returns the short time FFT at i,
        window width will be 1.5 * delta
        1 * delta after i and 0.5 * delta before
    """

    l= len(samples)
    if envelope is not None:
        spectrum = abs(scipy.fft(samples * envelope * scipy.hamming(l)))
    else:
        spectrum = abs(scipy.fft(samples))
    specL = len(spectrum)
    if equalize is not None:
        return spectrum[0:specL/2] * equalize
    else:
        return spectrum[0:specL/2]

def equalize(N, scale=-0.02):
    N_2 = N / 2
    f = lambda i: scale * scipy.log((N_2-i) * 1.0/N_2)
    return numpymap(f, range(0, N_2))

equalize=memoize(equalize)

def envelope(N, power=1):
    mult = scipy.pi / N
    f = lambda i: pow(0.5 + 0.5 * scipy.sin(i*mult - 1.5707963268), power)
    return numpymap(f, range(0, N))

envelope=memoize(envelope)
