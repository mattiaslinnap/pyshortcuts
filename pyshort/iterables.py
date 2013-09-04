#!/usr/bin/env python
"""
Utilities for working with data structures and iterables.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future_builtins import *  # ascii, filter, hex, map, oct, zip

import unittest


def successive(iterable, n=2):
    """Returns successive pairs or larger tuples of elements.
    With n=2: A B C D -> (A, B), (B, C), (C, D)
    With n=3: A B C D -> (A, B, C), (B, C, D)

    Useful for calculating deltas or "surrounding context" when iterating.
    """
    iterable = iter(iterable)
    # Prefill buffer of size n.
    buffer = []
    for i in xrange(n):
        buffer.append(iterable.next())
    # Buffer must be copied, so that caller can call list(successive()) if needed.
    # If it were returned in-place, all copies would keep changing.
    yield tuple(buffer)
    # Rotate buffer for all new elements.
    for elem in iterable:
        buffer.pop(0)
        buffer.append(elem)
        yield tuple(buffer)


def grouper(n, iterable):
    """Groups iterable into tuples. A B C D E -> (A,B) (C, D)"""
    assert n > 0
    args = [iter(iterable)] * n
    return zip(*args)


def igrouper(iterable, n):
    """Yields subiterables, each with n elements. A B C D E -> (A,B), (C, D), (E)."""
    assert n > 0
    it = iter(iterable)
    end = [False]  # end must be a mutable value, so that the inner() closure can modify it.
    def inner():
        i = 0
        for elem in it:
            yield elem
            i += 1
            if i >= n:
                break
        else:
            end[0] = True
    while not end[0]:
        yield inner()


def subsample(limit, lst):
    """Yields limit elements from lst, spaced at equal intervals. (as much as possible if the length does not divide exactly).
    Lst must support len(), can't be a pure iterable.
    """
    N = len(lst)
    assert limit > 0
    assert N >= limit
    
    yielded = 0
    passed = 0  # Including yielded elements
    for elem in lst:
        if limit * passed >= yielded * N:
            yield elem
            yielded += 1
        passed += 1


def avg(lst):
    """Average value of the list. Must support len()"""
    return sum(lst) / len(lst)


def first(iterable):
    return next(iter(iterable))


def last(iterable):
    if hasattr(iterable, '__getitem__'):
        return iterable[-1]
    else:
        lst = None
        for i in iterable:
            lst = i
        return lst


class IterablesTest(unittest.TestCase):
    def test_successive(self):
        self.assertEqual(list(successive([1, 2], n=2)), [(1, 2)])
        self.assertEqual(list(successive([1, 2, 3], n=2)), [(1, 2), (2, 3)])
        self.assertEqual(list(successive([1, 2, 3, 4], n=2)), [(1, 2), (2, 3), (3, 4)])

        self.assertEqual(list(successive([1, 2, 3], n=3)), [(1, 2, 3)])
        self.assertEqual(list(successive([1, 2, 3, 4], n=3)), [(1, 2, 3), (2, 3, 4)])

    def test_grouper(self):
        self.assertEqual(list(grouper(1, '')), [])
        self.assertEqual(list(grouper(1, 'ABCD')), [('A',), ('B',), ('C',), ('D',)])
        
        self.assertEqual(list(grouper(2, [])), [])
        self.assertEqual(list(grouper(2, 'ABCD')), [('A', 'B'), ('C', 'D')])        
        self.assertEqual(list(grouper(2, 'ABCDE')), [('A', 'B'), ('C', 'D')])
        
        self.assertEqual(list(grouper(3, 'ABCD')), [('A', 'B', 'C')])
        
    def test_subsample_small(self):
        self.assertEqual(list(subsample(1, 'A')), ['A'])
        self.assertEqual(list(subsample(1, 'ABCDE')), ['A'])
        self.assertEqual(list(subsample(2, 'ABCDE')), ['A', 'D'])
        self.assertEqual(list(subsample(3, 'ABCDE')), ['A', 'C', 'E'])
        self.assertEqual(list(subsample(4, 'ABCDE')), ['A', 'C', 'D', 'E'])
        self.assertEqual(list(subsample(5, 'ABCDE')), ['A', 'B', 'C', 'D', 'E'])
        
    def test_subsample_length(self):
        data = ['x'] * 1000
        for n in xrange(1, 1000):
            self.assertEqual(len(list(subsample(n, data))), n)  

    def test_avg(self):
        self.assertEqual(avg([5]), 5)
        self.assertEqual(avg([1,2,3]), 2)
        self.assertEqual(avg([2,3]), 2.5)


class FirstTest(unittest.TestCase):
    def test_list(self):
        self.assertEqual(1, first([1]))
        self.assertEqual(1, first([1,2,3]))

    def test_iter(self):
        def gen(lst):
            for i in lst:
                yield i

        self.assertEqual(1, first(gen([1])))
        self.assertEqual(1, first(gen([1,2,3])))

    def test_set(self):
        self.assertEqual(1, first(set([1])))
        self.assertEqual(1, first(set([1,2,3])))


class LastTest(unittest.TestCase):
    def test_list(self):
        self.assertEqual(1, last([1]))
        self.assertEqual(3, last([1,2,3]))

    def test_iter(self):
        def gen(lst):
            for i in lst:
                yield i
        self.assertEqual(1, last(gen([1])))
        self.assertEqual(3, last(gen([1,2,3])))

    def test_set(self):
        self.assertEqual(1, last(set([1])))
        self.assertIn(last(set([1,2,3])), [1,2,3])


if __name__ == '__main__':
    unittest.main()
