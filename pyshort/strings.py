#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import cStringIO
import gzip
import sys


def printf(fmt=None, *args, **kwargs):
    if fmt:
        print(fmt.format(*args, **kwargs))
    else:
        print()


def gunzip(gzdata):
    """Uncompresses gzip file data given as a string. The data is assumed to contain full gzip headers."""
    with gzip.GzipFile(mode='rb', fileobj=cStringIO.StringIO(gzdata)) as f:
        return f.read()


def color(text, col='r'):
    colorcode = {'r': '1;31',  # light red
                 'b': '1;34',  # light blue
                 'g': '1;32',  # light green
                 'c': '1;36',  # light cyan
                 'y': '1;33',  # yellow
                 'm': '1;35',  # light purple
                 'w': '1;37'   # white
                 }[col]
    return '\033[%sm%s\033[0m' % (colorcode, text)


def tabulate(rows, sep=' ', end='\n', join=True):
    """Takes a list of rows, each a list with equal number of column elements.
    """
    assert len(set(len(r) for r in rows)) == 1, 'All rows must have the same number of columns.'
    rows = [[unicode(c) for c in r] for r in rows]  # Map to strings.
    num_rows = len(rows)
    num_cols = len(rows[0])
    col_widths = [max(len(rows[ri][ci]) for ri in xrange(num_rows)) for ci in xrange(num_cols)]
    rows = [['{0:<{width}}'.format(r[ci], width=col_widths[ci]) for ci in xrange(num_cols)] for r in rows]  # Map to maximum-width column strings.
    text_rows = [sep.join(r) for r in rows]
    if join:
        return end.join(text_rows)
    else:
        return text_rows


# Global state for building up a table in quick scripts.

_TABLE_ROWS = []


def table_row(cols):
    global _TABLE_ROWS
    _TABLE_ROWS.append(cols)
    assert len(cols) == len(_TABLE_ROWS[0]), 'All rows must have the same number of columns. New is %d, old is %d.' % (len(cols), len(_TABLE_ROWS[0]))


def table_print(file=None, files=None, **kwargs):
    global _TABLE_ROWS

    if file and files:
        raise RuntimeError('Only one out of file and files can be given at a time.')
    if not files:
        files = [file] if file else [sys.stderr]

    table = tabulate(_TABLE_ROWS, **kwargs)
    for fname in files:
        if isinstance(fname, basestring):
            with open(fname, 'w') as f:
                print(table, file=f)
        else:
            # Expecting a file-like object or stream.
            print(table, file=fname)
    _TABLE_ROWS = []
