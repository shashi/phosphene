import os
from hashlib import sha1
import scipy.io.wavfile as wav
import pygame.mixer
from pygame.sndarray import make_sound

# Set mixer defaults
pygame.mixer.pre_init(44100, 16, 2, 4096)

__all__ = ["read", "makeSound"]

def digest(string):
    return sha1(string).hexdigest()

def read(fname):
    """ Reads an audio file into a numpy array.

        returns frequency, samples
    """
    # this is an ugly way to read mp3. But works well.
    # www.snip2code.com/Snippet/1767/Convert-mp3-to-numpy-array--Ugly--but-it
    suffix = digest(fname)[0:6]
    oname = '/tmp/tmp'+ suffix +'.wav'

    # ask lame to decode it to a wav file
    if not os.path.exists(oname):
        # Well, if you ctrl-c before conversion, you're going to
        # have to manually delete the file.
        cmd = 'lame --decode "%s" "%s"' % (fname, oname)
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

