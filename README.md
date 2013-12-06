Phosphene
=========

Phosphene is a library aimed at helping music visualization. This project is being written for visualizing music on a 10x10x10 3D LED display, and other hand-made devices (see apps/psychroom.py). But the phosphene package is more general and can be used for music visualization in general.

The Signal abstraction
----------------------

The Signal class provides some cool abstractions you can use to setup various attributes for a signal. You can initialize a signal from the raw wav data as shown below:

```python
from phosphene.signal import *
    # all example code below assumes that this line is on top
mySignal = Signal(data, sampling_rate)
    # data is usually a numpy array with
    # left & right channel samples
```

Now, `mySignal` has some time varying values like `mySignal.t`, the current time (unique for each `mySignal.x`); `mySignal.x`, the current sample number, (`mySignal.Y[mySignal.x]` is the current sample itself).

You can `lift` any function that takes the signal as argument to make it a time varying attribute of the same signal. e.g.:

```python
mySignal.xsquared = lift(lambda s: s.x**2)
```

Now, `mySignal.xsquared` is `mySignal.x` squared, and varies with `mySignal.x`.

You can also lift long sequences of the same length as the data in
the Signal. For example, the average of left and right channels in the data, `mySignal.A` is setup in this way in Signal's contructor.

```python
mySignal.A = lift((mySignal.Y[:, 0] + mySignal.Y[:, 1]) / 2)
    # average of left and right channels
```

referencing `mySignal.A` will return the `mySignal.x`th average value

You can also make these arrays "temporally indexable".

e.g. if you instead did

```python
mySignal.A = lift((mySignal.Y[:, 0] + mySignal.Y[:, 1]) / 2, True)
    # (the True argument makes it t-indexed)
```

`mySignal.A[0]` will be the `mySignal.x`th average value, while `mySignal.A[-1]` is the one before that,You can say `mySignal.A[-512:512]` to get 1024 values of `A` centered at the `mySignal.x`th sample

Using this, you can define short-time fft like this:

```python
mySignal.fft = lift(lambda s: dsp.fft(s.A[-N/2:N/2]))
```
where `N` is the size of your window for the STFFT.

A "process" is a function that takes a signal as its argument and affects the world (e.g. draws something trippy on the screen). Processes can "perceive" a signal. `perceive` simulates changes in the signal as if it is being read in real-time. Watch.

```python
from phosphene.graphs import *
def barsProcess(s):
    surface.fill((0, 0, 0))
    print "The current sample number is:", s.x
    print "The current fps is:", s.fps
    # Plot the short-time FFT in a bar graph
    barGraph(surface, (0, 0, 640, 480), group(32, s.fft))
    display.update()

# assuming mySingal is loaded and all the code above is
# executed
processes = [barsProcess]
song.play() # start playing the music that will be perceived, this call needs to be non blocking
fps = 90 # the fps you'd like (actual fps maybe lesser)
perceive(processes, mySingal, fps) # simulate perception of music by processes
```

`signal` and `signalutil` modules contain some functions that return `lift` values. Such as `foldp` (fold over past) and `blend` (cause a value vary smoothly).

See demo.py for an example of beat detection done using this class and some utility functions from phosphene.

Happy Hacking!

dependencies
------------

* Python 2.x
* numpy, scipy and pygame python packages
* lame
