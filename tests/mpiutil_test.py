#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for MPI utility class.
'''

import unittest

from gaft.mpiutil import mpi


class MPIUtilTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_split(self):
        seq = list(range(10))

        if mpi.size == 1:
            self.assertListEqual(mpi.split(seq), seq)
        elif mpi.size == 2:
            if mpi.rank == 0:
                self.assertListEqual(mpi.split(seq), [0, 1, 2, 3, 4])
            elif mpi.rank == 1:
                self.assertListEqual(mpi.split(seq), [5, 6, 7, 8, 9])

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(MPIUtilTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

