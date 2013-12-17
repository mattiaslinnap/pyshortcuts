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


def color(text, col='r'):
    """Returns text surrounded by Bash terminal colour codes. Useful for easier to notice errors in long outputs."""
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
    """Makes an ASCII-formatted table.
    Rows must be a list of rows, each a list with equal number of column elements.
    Elements can be of any type, they are converted to strings before finding maximum width of each column.

    For copy-pasting tables into LaTeX, set sep=' & ' and end='\\\\\n'.
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

