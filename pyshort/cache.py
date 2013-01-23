"""Caching for arbritary functions.
Useful for slow data-parsing code.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import cPickle
from decorator import decorator
import os
import sys

CACHES_BASE = '/local/scratch/ml421/caches'

def cached(project, key_format):
    """Caching decorator for slow functions.

    Usage:
    @cached(project name (used as directory), key format string (used as filename))
    def slow(...):
        pass

    Key format string can include positional args with {0} and keyword args {name} from the function call.
    A special keyword arg func_name is added to the formatting parameters.
    """
    def caching(func, *args, **kwargs):
        key = key_format.format(*args, **dict(kwargs, func_name=func.__name__))
        dirname = os.path.join(CACHES_BASE, project)
        if not os.path.exists(dirname):
            os.mkdir(dirname, 0755)
        filename = os.path.join(dirname, key + '.pickle')
        try:
            with open(filename, 'rb') as f:
                return cPickle.load(f)
        except IOError:
            print('No cache for {0}/{1}, running slow function.'.format(project, key), file=sys.stderr)
            data = func(*args, **kwargs)
            with open(filename, 'wb') as f:
                cPickle.dump(data, f, -1)
            return data
    return decorator(caching)
