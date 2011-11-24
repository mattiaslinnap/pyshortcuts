#!/usr/bin/python
'''
Utilities for working with data structures and iterables.
'''
from __future__ import division

from itertools import izip
import unittest2

def grouper(n, iterable):
    """Groups iterable into tuples. A B C D E -> (A,B) (C, D)"""
    assert n > 0
    args = [iter(iterable)] * n
    return izip(*args)

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


class IterablesTest(unittest2.TestCase):
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

if __name__ == '__main__':
    unittest2.main()
