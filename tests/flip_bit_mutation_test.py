#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for built-in Flip Bit mutation operator.
'''

import unittest

from gaft.components.individual import GAIndividual
from gaft.operators.mutation.flip_bit_mutation import FlipBitMutation

class FlipBitMutationTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff

    def test_mutate(self):
        ''' Make sure the individual can be mutated correctly.
        '''
        indv = GAIndividual(ranges=[(0, 1)]).init(variants=[0.398])
        mutation = FlipBitMutation(pm=1.0)
        chromsome_before = [0, 1, 1, 0, 0, 1, 0, 1, 1]
        chromsome_after = [1, 0, 0, 1, 1, 0, 1, 0, 0]
        self.assertListEqual(indv.chromsome, chromsome_before)
        mutation.mutate(indv)
        self.assertListEqual(indv.chromsome, chromsome_after)

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(FlipBitMutationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

