#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Utitlities for parallelize Genetic Algorithm by using MPI interfaces
in distributed MPI environment.
'''

from itertools import chain

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
    def split_seq(self, sequence):
        '''
        Split the sequence according to rank and processor number.
        '''
        starts = [i for i in range(0, len(sequence), len(sequence)//self.size)]
        ends = starts[1: ] + [len(sequence)]
        start, end = list(zip(starts, ends))[self.rank]

        return sequence[start: end]

    def split_size(self, size):
        '''
        Split a size number(int) to sub-size number.
        '''
        if size % self.size != 0:
            splited_sizes = [size // self.size]*self.size + [size % self.size]
        else:
            splited_sizes = [size // self.size]*self.size

        return splited_sizes[self.rank]

    def merge_seq(self, seq):
        '''
        Gather data in sub-process to root process.
        '''
        if self.size == 1:
            return seq

        mpi_comm = MPI.COMM_WORLD
        merged_seq= mpi_comm.allgather(seq)
        return list(chain(*merged_seq))


mpi = MPIUtil()

