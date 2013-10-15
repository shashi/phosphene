import scipy
import numpy
import pygame
from pygame import display
from pygame.draw import *
from pygame import Color
import math

def barGraph(surface, rectangle, data, transform=lambda y: scipy.log(y + 1)):
    """
        drawing contains (x, y, width, height)
    """
    x0, y0, W, H = rectangle

    l = len(data)
    w = W / l
    m = transform(max(data))
    for i in range(0, l):
        if m > 0:
            p = transform(data[i])
            h = p * 5
            hue = p / m
            c = Color(0, 0, 0, 0)
            c.hsva = ((1-hue) * 360, 100, 100, 0)
            x = x0 + i * w
            y = y0 + H - h
            rect(surface, c, \
                    (x, y, 0.9 * w, h))
def circleRays(surface, center, data, transform=lambda y: scipy.log(y + 1)):

    x0, y0 = center
    
    total = math.radians(360)
    l = len(data)
    m = transform(max(data))
    part = total/l
    for i in range(0, l):
        if m > 0:
            p = transform(data[i])
            h = p * 5
            hue = p / m
            c = Color(0, 0, 0, 0)
            c.hsva = ((1-hue) * 360, 100, 100, 0)
            x = x0 + h*math.cos(part * i)
            y = y0 + h*math.sin(part*i)
            line(surface, c, 
                    (x0,y0),(x,y),1)


