import os
import string
import time
import random
from hashlib import sha1
import scipy.io.wavfile as wav
import pygame.mixer
from pygame.sndarray import make_sound

# Set mixer defaults
pygame.mixer.pre_init(44100, 16, 2, 4096)

__all__ = ["read", "makeSound", "playAndRun"]

def digest(string):
    return sha1(string).hexdigest()

def getTime(since=0):
    return time.time()-since


def read(fname):
    """ Reads an audio file into a numpy array.

        returns frequency, samples
    """
    # this is an ugly way to read mp3. But works well.
    # www.snip2code.com/Snippet/1767/Convert-mp3-to-numpy-array--Ugly--but-it
    suffix = digest(fname)[0:6]
    oname = '/tmp/tmp'+ suffix +'.wav'
    # ask lame to decode it to a wav file
    cmd = 'lame --decode %s %s' % (fname, oname)
    os.system(cmd)

    # now read using scipy.io.wavfile
    data = wav.read(oname)
    # return samplingFrequency, samples
    return data[0], data[1]

def makeSound(samplingFreq, data):
    """ Make a Player object from raw data

        returns a pygame.mixer.Sound object
    """
    # Ugh! impurity
    pygame.mixer.init(frequency=samplingFreq)
    return make_sound(data)

def playAndRun(sound, loop, cps=60):
    """ Takes a pygame.mixer.Sound object, a loop function and preferred cps,
        tries to execute the loop function cps times every second.
        loop gets the approximate sample number as argument when the song
        is being played.
    """
    # this will help me make sure only one file is being played
    assert(not pygame.mixer.get_busy())
    sF = pygame.mixer.get_init()[0]
    callSpacing = 1.0 / cps
    sound.play()
    prev_i = -1
    # Cheap hack for finding the sample we are playing.
    try:
        start = getTime()
        while pygame.mixer.get_busy():
            tic = getTime()
            i = int((tic-start) * sF)
            loop(i, sF / float(i - prev_i))
            prev_i = i
            # atrocious assumptions, but they'll serve the purpose
            toc = getTime()
            wait = (tic + callSpacing - toc)
            # chill out before looping.
            if wait > 0: time.sleep(wait)
        return True
    finally:
        sound.stop() # stop playing if you're going to error out.
