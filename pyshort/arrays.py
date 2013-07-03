#!/usr/bin/env python
"""
Utilities for Numpy arrays.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import numpy as np
import unittest

from pyshort.iterables import first, last


def map_to_small_integers(arr):
    """Returns an int32 array of len(arr), with each unique element mapped to an unique dense integer.
    The integers are assigned from 0, counting in sorted order of the initial array.
    """
    sorted_unique, inverse = np.unique(arr, return_inverse=True)
    return inverse


def split_nonzero(arr):
    """Yields [start,end) indexes for sections where the boolean array is zero.

    Sections start at index 0 or whenever array is > 0, and end with index -1 or before the next array > 0.
    Sections of length < 2 are omitted.
    """
    if len(arr) < 2:
        return np.array([], dtype=int)

    arr = arr.astype(bool)
    arr = arr.astype('int8')
    diff = np.diff(arr)  # -1, 0 and 1
    idxs, = np.nonzero(diff)  # Indexes of -1 and 1

    splits = []
    start = 0

    for idx in idxs:
        if diff[idx] == -1:  # Changed from nonzero to zero. Start of new split.
            start = idx
        elif idx > start:  # Changed from zero to nonzero. End of a split if it isn't too short
            splits.append((start, idx + 1))
    # If ended on a zero, perhaps add last slice.
    if not arr[-1]:
        splits.append((start, len(arr)))

    return np.array(splits, dtype=int)


class SplitNonzeroTest(unittest.TestCase):

    def assertSplit(self, expected_indices, argument):
        expect = np.array(expected_indices, dtype=int)
        result = split_nonzero(np.array(argument, dtype=int))
        self.assertTrue(np.array_equal(expect, result),
                        'Expected\n{}\ngot\n{}'.format(expect, result))

    def test_empty(self):
        self.assertSplit([], [])

    def test_one_zero(self):
        self.assertSplit([], [0])

    def test_one_nonzero(self):
        self.assertSplit([], [5])

    def test_two_zeros(self):
        self.assertSplit([(0, 2)], [0, 0])

    def test_two_nonzeros(self):
        self.assertSplit([], [3, 4])

    def test_two_mixed(self):
        self.assertSplit([], [0, 4])
        self.assertSplit([(0, 2)], [3, 0])

    def test_start_nonzero(self):
        self.assertSplit([(1, 3)], [1, 5, 0, 2])

    def test_start_zero(self):
        self.assertSplit([(0 ,2)], [0, 0, 4, 3])

    def test_end_nonzero(self):
        self.assertSplit([(0 ,3)], [0, 0, 0, 1])

    def test_end_zero(self):
        self.assertSplit([(0, 4)], [3, 0, 0, 0])

    def test_no_shorts(self):
        self.assertSplit([(0, 2), (2, 5), (5, 7)], [0, 0, 3, 0, 0, 3, 0])

    def test_shorts(self):
        self.assertSplit([(1, 3), (4, 6)], [0, 3, 0, 3, 3, 0])

    def test_all_nonzero(self):
        self.assertSplit([], [1, 3, 1, 3, 3, 1])

    def test_all_zero(self):
        self.assertSplit([(0, 5)], [0, 0, 0, 0, 0])

if __name__ == '__main__':
    unittest.main()
