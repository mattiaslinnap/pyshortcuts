#!/usr/bin/python
'''
Statistical functions and helpers.
'''
from __future__ import division

import unittest2


def tanimoto(set1, set2):
    """Computes the Tanimoto set similarity (not exactly Tanimoto Coefficient).
    
    http://en.wikipedia.org/wiki/Jaccard_index
    Equal to size of intersection / size of union. Undefined for two empty sets."""
    return len(set1 & set2) / len(set1 | set2)



class StatsTest(unittest2.TestCase):
    def test_tanimoto(self):
        self.assertEqual(tanimoto(set([1,2,3]), set([1,2,3])), 1)
        self.assertEqual(tanimoto(set([1,2,3]), set([4,5,6])), 0)
        
        self.assertEqual(tanimoto(set([1,2,3]), set([2,3,4])), 0.5)
        self.assertEqual(tanimoto(set([1,2,3,4,5]), set([5,6,7,8,9])), 1 / 9)
        
        self.assertEqual(tanimoto(set(), set([1,2,3])), 0)
        self.assertEqual(tanimoto(set([1,2,3]), set()), 0)
        
if __name__ == '__main__':
    unittest2.main()
