#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Utitlities for parallelize Genetic Algorithm by using MPI interfaces
in distributed MPI environment.
'''

try:
    from mpi4py import MPI
    MPI_INSTALLED = True
except ImportError:
    MPI_INSTALLED = False


class MPIUtil(object):
    def __init__(self):
        # Nothing here.
        pass

    # Wrapper for common MPI interfaces.
    def barrier(self):
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            mpi_comm.barrier()

    @property
    def rank(self):
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            return mpi_comm.Get_rank()
        else:
            return 0

    @property
    def size(self):
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            return mpi_comm.Get_size()
        else:
            return 1

    @property
    def is_master(self):
        return self.rank == 0

    # Utility methods.
    def split(self, sequence):
        '''
        Split the sequence according to rank and processor number.
        '''
        starts = [i for i in range(0, len(sequence), len(sequence)//self.size)]
        ends = starts[1: ] + [len(sequence)]
        start, end = list(zip(starts, ends))[self.rank]

        return sequence[start: end]


mpi = MPIUtil()

