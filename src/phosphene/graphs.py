import pdb
import scipy
import numpy
import pygame
from pygame import display
from pygame.draw import *
from pygame import Color
import math

def barGraph(data):
    """
        drawing contains (x, y, width, height)
    """

    def f(surface, rectangle):
        x0, y0, W, H = rectangle
        try:
            l = len(data)
        except:
            pdb.set_trace()
        w = W / l
        try:
            for i in range(0, l):
                h = data[i]
                c = Color(0, 0, 0, 0)
                c.hsva = (0, 100, 100, 0)
                x = x0 + i * w
                y = y0 + H * (1 - h)
                rect(surface, c, \
                        (x, y, 0.9 * w, h * H))
        except:
            pdb.set_trace()
    return f

def boopGraph(data):
    def f(surface, rectangle):
        x0, y0, W, H = rectangle
        try:
            l = len(data)
        except:
            pdb.set_trace()
        dx = W / l
        try:
            for i in range(0, l):
                d = data[i]
                a = dx * d
                x = (dx - a) / 2 + i * dx + x0
                y = (H - dx) / 2 + (dx - a) / 2 + y0
                c = Color(255, 255, 255, 255)
                rect(surface, c, \
                        (x, y, a, a))
        except:
            pdb.set_trace()
    return f


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
            x = x0 + (m*2+h)*math.cos(part * i)
            y = y0 + (m*2+h)*math.sin(part*i)
            line(surface, c, 
                    (x0,y0),(x,y),1)
            circle(surface,c, center,int(m*2),0)
   
def graphsGraphs(graphs, direction=0):
    def f(surface, bigRect):
        x0, y0, W, H = bigRect
        h = H / len(graphs)
        for graph in graphs:
            graph(surface, (x0, y0, W, h))
            y0 += h
    return f
