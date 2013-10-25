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

    return numpy.array(
            [sum(fft[splitIdx[i-1]:splitIdx[i]]) for i in range(1, n + 1)])

def fft(samples, out_n, env=None, eq=None):
    """
        Returns the short time FFT at i,
        window width will be 1.5 * delta
        1 * delta after i and 0.5 * delta before
    """

    in_n = len(samples)
    if env:
        spectrum = abs(scipy.fft(samples * scipy.hamming(in_n) * envelope(in_n)))
    else:
        spectrum = abs(scipy.fft(samples))

    if out_n:
        if eq:
            return group(out_n, spectrum[0:0.9*in_n/2]) * equalize(out_n)
        else:
            return group(out_n, spectrum[0:0.9*in_n/2])
    else:
        if eq:
            return spectrum[0:in_n/2] * equalize(in_n/2)
        else:
            return spectrum[0:in_n/2]

def equalize(N, scale=-0.02):
    f = lambda i: scale * scipy.log((N-i) * 1.0/N)
    return numpymap(f, range(0, N))

equalize=memoize(equalize)

def envelope(N, power=1):
    mult = scipy.pi / N
    f = lambda i: pow(0.5 + 0.5 * scipy.sin(i*mult - scipy.pi / 2), power)
    return numpymap(f, range(0, N))

envelope=memoize(envelope)
