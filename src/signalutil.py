import pdb
import scipy
import numpy

def getFFTIdx(Fs, Hz, n):
    assert(Hz <= Fs / 2);
    return round(Fs / n * Hz)

def getNotes():
    return [0] \
           + [16.35 * pow(2, i/12.0) + 1 for i in range(0, 101)] \
           + [11050, 22100]

def bin(n, fft, grouping=lambda i: i):
    """
        Put fft data into n bins by adding them.

        grouping function defines how things are grouped
        lambda i: i       --> linear grouping
        lambda i: 2 ** i  --> logarithmic
    """
    # discard second half -- useless by
    # Nyquist criteria

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

def getSFFT(data, i, w, window=scipy.hamming):
    """
        Returns the short time FFT at i,
        window width will be 1.5 * delta
        1 * delta after i and 0.5 * delta before
    """

    l = len(data)
    start = max(0, i - w * 1 / 2 - 1);
    end = min(i + w * 1 / 2, l)
    samples = data[start:end]
    if hasattr(window, '__call__'):
        envelope = window(len(samples))
    else:
        envelope = window

    l= len(samples)
    try:
        spectrum = abs(scipy.fft(envelope * samples))
    except:
        spectrum = abs(scipy.fft(samples))
    specL = len(spectrum)
    return spectrum[0:specL/2]
