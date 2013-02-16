#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import cStringIO
import gzip

def printf(fmt=None, *args, **kwargs):
    if fmt:
        print(fmt.format(*args, **kwargs))
    else:
        print()

def gunzip(gzdata):
    """Uncompresses gzip file data given as a string. The data is assumed to contain full gzip headers."""
    with gzip.GzipFile(mode='rb', fileobj=cStringIO.StringIO(gzdata)) as f:
        return f.read()