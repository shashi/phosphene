import sys
import pygame
from pygame import display
from pygame.draw import *
import scipy
import time

from phosphene import audio
from phosphene.util import *
from phosphene.signal import *
from phosphene.dsp import *
from phosphene.graphs import *

pygame.init()
surface = display.set_mode((640, 480))

if len(sys.argv) < 2:
    print "Usage: %s file.mp3" % sys.argv[0]
    sys.exit(1)
else:
    fPath = sys.argv[1]

sF, data = audio.read(fPath)

def test_process(s):
    surface.fill((0, 0, 0))
    barGraph(surface, (0, 0, 640, 480), group(32, s.fft)[:-8])
    display.update()
    print s.fps

processes = [test_process]

S = Signal(data, sF)

S.A = lift((data[:,0] + data[:,1]) / 2, True)

N = 2048
S.fft = lift(lambda s: fft(s.A[-N/4:3*N/4], envelope(N), equalize(N)))

soundObj = audio.makeSound(sF, data)
soundObj.play()
perceive(processes, S, 90)
