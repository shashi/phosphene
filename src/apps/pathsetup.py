import os, sys

dirname = os.path.dirname
here = os.path.abspath(__file__)
parentdir = dirname(dirname(here))
sys.path.append(parentdir)
