phosphene
=========

phosphene is a library aimed at helping music visualization. This project is being written for visualizing music on a 10x10x10 3D LED display. Hopefully it can be made into something more general that is useful for other problems involving music visualization.

The Signal abstraction
----------------------

The Signal class is awesome. You initialize a signal like this:

```python
from phosphene.signal import *
    # all example code below assumes that this line is on top
mySignal = Signal(data, sampling_rate)
    # data is usually a numpy array with
    # left & right channel samples
```

Now, s has some time varying values like `mySignal.t`, the current time (unique for each `mySignal.x`); `mySignal.x`, the current sample.

You can lift any function to make it a time varying value associated with the signal. e.g.:

```python
mySignal.xsquared = lift(lambda s: s.x**2)
```

Now, `mySignal.xsquared` is `mySignal.x` squared, and varies with `mySignal.x`.

You can also lift long sequences of the same length as the data in
the Signal:

```python
mySignal.A = lift((mySignal.Y[:, 0] + mySignal.Y[:, 1]) / 2)
    # average of left and right channels
```

referencing `mySignal.A` will return the `mySignal.x`th average value

You can also make these arrays "temporally indexable".

e.g. if you instead did

```python
mySignal.A = lift((mySignal.Y[:, 0] + mySignal.Y[:, 1]) / 2, True)
    # (the True argument means make it t-indexed)
```

`mySignal.A[0]` will be the mySignal.xth average value, mySignal.A[-1] is the one before that,You can say `mySignal.A[-512:512]` to get 1024 values in A centered at `mySignal.x`th sample

Using this, you can define short-time fft like this:

```python
mySignal.fft = lift(lambda s: dsp.fft(s.A[-N/2:N/2]))
```
where `N` is the size of your window for the STFFT.

Finally, processes can "perceive" a signal:

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
perceive(processes, mySingal, fps)
```

here, `processes` is a list of functions that do something with the current value of `s`, the signal being perceived. `perceive` simulates changes in the signal as if it is being read in real-time. see player.py for a working example use of the Signal abstraction.

Happy Hacking!

dependencies
------------

* Python 2.7
* numpy, scipy and pygame python packages
