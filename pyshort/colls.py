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
    >>> a = deepdict({2: {u'foo': {u'baz': 30}}}); a[2][u'foo'][u'bar'] = 20; a
    {2: {u'foo': {u'bar': 20, u'baz': 30}}}

    To catch bugs, overwriting a generated dict is not allowed:
    >>> a = deepdict(); a[1][u'foo'] = 10; a[1] = 20
    Traceback (most recent call last):
    ...
    ValueError: Refusing to overwrite existing dictionary.
    """

    def __init__(self, initial=None):
        """If initial dictionary is given, it is recursively converted into deepdicts."""
        if initial is not None:
            for key in initial:
                if isinstance(initial[key], dict):
                    self[key] = deepdict(initial[key])
                else:
                    self[key] = initial[key]

    def __missing__(self, key):
        self[key] = deepdict()
        return self[key]

    def __setitem__(self, key, value):
        if key in self and isinstance(self[key], dict):
            raise ValueError('Refusing to overwrite existing dictionary.')
        return super(deepdict, self).__setitem__(key, value)

    def __getattr__(self, name):
        """Only used if the attribute does not otherwise exist on the object."""
        return self[name]

if __name__ == '__main__':
    import doctest
    doctest.testmod()

