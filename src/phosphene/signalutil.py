# Functions to help you lift and fold
from .signal import *
import numpy
import pdb

def expAvg(f, ratio=lambda s: 0.5):
    """Create the exponential averaging of a signal attribute"""
    # ratio = (lambda s: ratio) if isinstance(ratio, float) else ratio

    g = (lambda s: getattr(s, f)) if isinstance(f, str) else f
    h = (lambda s: ratio) if isinstance(ratio, float) else ratio

    return foldp(lambda s, prev: (g(s) * h(s) + \
            prev[1] * (1-h(s)), prev[0]), (numpy.array([0]), numpy.array([0])))

