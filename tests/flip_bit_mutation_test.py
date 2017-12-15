#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for built-in Flip Bit mutation operator.
'''

import unittest

from gaft.components import BinaryIndividual, DecimalIndividual
from gaft.operators.mutation.flip_bit_mutation import FlipBitMutation

class FlipBitMutationTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff

    def test_mutate_binary_indv(self):
        ''' Make sure the individual can be mutated correctly.
        '''
        indv = BinaryIndividual(ranges=[(0, 1)]).init(solution=[0.398])
        mutation = FlipBitMutation(pm=1.0)
        chromsome_before = [0, 1, 1, 0, 0, 1, 0, 1, 1]
        chromsome_after = [1, 0, 0, 1, 1, 0, 1, 0, 0]
        self.assertListEqual(indv.chromsome, chromsome_before)
        mutation.mutate(indv, engine=None)
        self.assertListEqual(indv.chromsome, chromsome_after)

    def test_mutate_decimal_indv(self):
        ''' Make sure individual with decimal encoding can be mutated correctly.
        '''
        indv = DecimalIndividual(ranges=[(0, 1), (0, 2)]).init(solution=[0.5, 1.5])
        mutation = FlipBitMutation(pm=1.0)
        chromsome_before = [0.5, 1.5]
        self.assertListEqual(indv.chromsome, chromsome_before)
        mutation.mutate(indv, engine=None)
        for a, b in zip(indv.chromsome, chromsome_before):
            self.assertNotEqual(a, b)

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(FlipBitMutationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

