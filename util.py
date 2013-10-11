import os
import string
import random
from hashlib import sha1
import scipy.io.wavfile as wav
from pygame.sndarray import make_sound

def digest(string):
    return sha1(string).hexdigest()

def audioread(fname):
    # this is an ugly way to read mp3. But works well.
    # www.snip2code.com/Snippet/1767/Convert-mp3-to-numpy-array--Ugly--but-it
    suffix = digest(fname)[0:6]
    oname = '/tmp/tmp'+ suffix +'.wav'
    # ask lame to decode it to a wav file
    cmd = 'lame --decode %s %s' % (fname, oname)
    os.system(cmd)

    # now read using scipy.io.wavfile
    return wav.read(oname)

def makePlayer(samplingFreq, data):
    return make_sound(data)
