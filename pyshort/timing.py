from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

from decorator import decorator
import time
import sys

@decorator
def print_runtime(func, *args, **kwargs):
    start = time.time()
    try:
        return func(*args, **kwargs)
    finally:
        elapsed = time.time() - start
        print('{0} exec time {1:.3f} seconds.'.format(func.__name__, elapsed), file=sys.stderr)


