#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for GAIndividual
'''

import unittest

from gapy.components.individual import GAIndividual

class IndividualTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_binary_encoding(self):
        ''' Make sure individual can decode and encode binary gene correctly.
        '''
        indiv = GAIndividual(variants=[0.398], ranges=[(0, 1)],
                             encoding='binary', eps=0.001)

        # Test binary chromsome.
        ref_chromsome = [0, 1, 1, 0, 0, 0, 1, 1, 1, 0]
        self.assertListEqual(indiv.chromsome, ref_chromsome)

        # Test decode.
        self.assertListEqual(indiv.decode(), [0.398])

        indiv = GAIndividual(variants=[0.398, 0.66], ranges=[(0, 1), (-1, 1)],
                             encoding='binary', eps=0.001)

        # Test binary chromsome.
        ref_chromsome = [0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0]
        self.assertListEqual(indiv.chromsome, ref_chromsome)

        # Test decode.
        self.assertListEqual(indiv.decode(), [0.398, 0.6600000000000001])

    def test_decimal_construction(self):
        ''' Make sure individual can decode and encode decimal gene correctly.
        '''
        indiv = GAIndividual(variants=[0.398], ranges=[(0, 1)],
                             encoding='decimal', eps=0.001)
        self.assertListEqual(indiv.encode(), [0.398])
        self.assertListEqual(indiv.decode(), [0.398])

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(IndividualTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

