import scipy
import numpy
import pygame
from pygame import display
from pygame.draw import *

def bin(n, fft, grouping=lambda i: i):
    """
        Put fft data into n bins by adding them.

        grouping function defines how things are grouped
        lambda i: i       --> linear grouping
        lambda i: 2 ** i  --> logarithmic
    """
    # discard second half -- useless by
    # Nyquist criteria

    l = len(fft)
    fft = abs(fft)
    points = fft[0:l/2 - 1]
    N = l / 2
    k = N / n

    splitPoints = numpy.array([grouping(i) for i in range(0, n + 1)], dtype=float)
    splitIdx = splitPoints / abs(max(splitPoints)) * N
    splitIdx = [int(i) for i in splitIdx]
    return [sum(fft[splitIdx[i-1]:splitIdx[i]]) for i in range(1, n + 1)]
    
WHITE = (255, 255, 255)
def barGraph(surface, rectangle, data):
    """
        drawing contains (x, y, width, height)
    """
    x0, y0, W, H = rectangle

    l = len(data)
    w = W / l
    m = max(data)
    for i in range(0, l):
        h = scipy.log(abs(data[i])+1) * 20
        x = x0 + i * w
        y = H - h
        rect(surface, WHITE, (x, y, 0.9 * w, h))

def average(data):
    if len(data) > 1:
        l = len(data[0])
        return map(lambda r: sum(r) / l, data)
    else: return []

def getSFFT(data, i, w):
    """
        Returns the short time FFT at i,
        window width will be 1.5 * delta
        1 * delta after i and 0.5 * delta before
    """

    l = len(data)
    start = max(0, i - w * 1 / 2);
    end = min(i + w * 1 / 2, l)
    samples = average(data[start:end])
    window = scipy.hamming(len(samples))

    return scipy.fft(window * samples)

