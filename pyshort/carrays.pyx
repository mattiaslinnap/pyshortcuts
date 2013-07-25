#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import numpy as np
cimport cython
cimport numpy as np


def bincount2d(np.ndarray[int] xs, np.ndarray[int] ys, width=None, height=None):
    """Returns a 2d array of counts of elements at each coordinate.

    Any x or y values outside range 0...width and 0...height are ignored.
    If width or height are not given, max of xs and ys is used.
    """
    assert len(xs) == len(ys)
    assert len(xs) < 2000000000  # Limits of int32
    assert len(ys) < 2000000000

    cdef int w = width or xs.max() + 1
    cdef int h = height or ys.max() + 1
    cdef np.ndarray[int, ndim=2] count = np.zeros((h, w), dtype=np.int32)
    cdef int i
    cdef int x
    cdef int y
    for i in range(len(xs)):
        x = xs[i]
        y = ys[i]
        if 0 <= x < w and 0 <= y < h:
            count[y, x] += 1
    return count
