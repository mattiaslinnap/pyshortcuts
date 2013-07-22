#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip


class deepdict(dict):
    """A defaultdict of infinitely recursive defaultdicts.

    Examples:
    >>> a = deepdict(); a[1] = 10; a
    {1: 10}
    >>> a = deepdict(); a[2][u'foo'][u'bar'] = 20; a
    {2: {u'foo': {u'bar': 20}}}

    To catch bugs, overwriting a generated dict is not allowed:
    >>> a = deepdict(); a[1][u'foo'] = 10; a[1] = 20
    Traceback (most recent call last):
    ...
    ValueError: Refusing to overwrite existing dictionary.
    """

    def __missing__(self, key):
        self[key] = deepdict()
        return self[key]

    def __setitem__(self, key, value):
        if key in self and isinstance(self[key], dict):
            raise ValueError('Refusing to overwrite existing dictionary.')
        return super(deepdict, self).__setitem__(key, value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

