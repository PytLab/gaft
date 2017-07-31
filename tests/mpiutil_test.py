#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for MPI utility class.
'''

import unittest

from gaft.mpiutil import mpi


class MPIUtilTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_split_seq(self):
        seq = list(range(10))

        if mpi.size == 1:
            self.assertListEqual(mpi.split_seq(seq), seq)
        elif mpi.size == 2:
            if mpi.rank == 0:
                self.assertListEqual(mpi.split_seq(seq), [0, 1, 2, 3, 4])
            elif mpi.rank == 1:
                self.assertListEqual(mpi.split_seq(seq), [5, 6, 7, 8, 9])

    def test_merge_seq(self):
        if mpi.size == 1:
            self.assertListEqual(mpi.merge_seq([1, 2, 3]), [1, 2, 3])
        if mpi.size == 2:
            if mpi.rank == 0:
                recv_data = mpi.merge_seq([1, 2, 3])
            elif mpi.rank == 1:
                recv_data = mpi.merge_seq([2, 3, 4])
            self.assertListEqual(recv_data, [1, 2, 3, 2, 3, 4])

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(MPIUtilTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

