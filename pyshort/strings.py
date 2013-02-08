#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip


def printf(fmt=None, *args, **kwargs):
    if fmt:
        print(fmt.format(*args, **kwargs))
    else:
        print()
