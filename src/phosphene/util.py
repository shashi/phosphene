import numpy
from threading import Thread # this is for the repl

__all__ = ['memoize', 'memoizeBy', 'numpymap', 'indexable', 'reverse']
# Helper functions
def memoize(f, key=None):
    mem = {}
    def g(*args):
        k = str(args)
        if mem.has_key(k):
            return mem[k]
        else:
            r = f(*args)
            mem[k] = r
            return r
    return g

def memoizeBy(f, x, *args):
    # memoize by something else.
    return memoize(lambda k: f(*args))(x)

def numpymap(f, X):
    " returns a numpy array after maping "
    return numpy.array(map(f, X))

def indexable(f, offset=0):
    " make a list-like object "
    if not hasattr(f, '__call__'):
        # XXX: Assuming f is a sequence type
        try: f[0]
        except:
            raise "Are you sure what you are trying" + \
                  "to make indexable is a function or" + \
                  "a sequence type?"
        g = f
        f = lambda i: g[i] # LOL

    class Indexable:
        def getFunction(self):
            return f
        def __getitem__(self, *i):
            if len(i) == 1:
                i = i[0]
                if isinstance(i, int):
                    return f(i + offset)
                    # Handle range queries
                elif isinstance(i, slice):
                    return [f(j + offset) for j in \
                            range(i.start, i.stop, 1 if i.step is None else 0)]
            else:
                raise "You will have to implement that crazy indexing."
        def __len__(self):
            return 0

    return Indexable()

def windowedMap(f, samples, width, overlap):
    return res

def reverse(l):
    m = [c for c in l]
    m.reverse()
    return m

