#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
A high-level utility class for parallelizing Genetic Algorithm by using MPI interfaces
in distributed MPI environment.
'''

import logging
from itertools import chain
from functools import wraps

try:
    from mpi4py import MPI
    MPI_INSTALLED = True
except ImportError:
    MPI_INSTALLED = False


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class MPIUtil(object):

    __metaclass__ = Singleton

    def __init__(self):
        ''' Wrapper class for higher level of MPI interfaces that will create a
        singleton for parallelization.
        '''
        logger_name = 'gaft.{}'.format(self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)

    def bcast(self, data):
        ''' Broadcast data to MPI processes

        :param data: Data to be broadcasted
        :type data: any Python object
        '''
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            bdata = mpi_comm.bcast(data, root=0)
        else:
            bdata = data
        return bdata

    # Wrapper for common MPI interfaces.
    def barrier(self):
        ''' Block until all processes in the communicator have reached this routine
        '''
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            mpi_comm.barrier()

    @property
    def rank(self):
        ''' Get the rank of the calling process in the communicator
        '''
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            return mpi_comm.Get_rank()
        else:
            return 0

    @property
    def size(self):
        ''' Get the size of the group associated with a communicator
        '''
        if MPI_INSTALLED:
            mpi_comm = MPI.COMM_WORLD
            return mpi_comm.Get_size()
        else:
            return 1

    @property
    def is_master(self):
        ''' If current process is the master process
        '''
        return self.rank == 0

    # Utility methods.
    def split_seq(self, sequence):
        ''' Split the sequence according to rank and processor number.

        :param sequence: Data sequence to be splitted
        :type sequence: any Python object list

        :return: Sub data sequence for current process
        :rtype: any Python object list
        '''
        starts = [i for i in range(0, len(sequence), len(sequence)//self.size)]
        ends = starts[1: ] + [len(sequence)]
        start, end = list(zip(starts, ends))[self.rank]

        return sequence[start: end]

    def split_size(self, size):
        ''' Split a size number(int) to sub-size number.

        :param size: The size number to be splitted.
        :type size: int

        :return: Sub-size for current process
        :rtype: int
        '''
        if size < self.size:
            warn_msg = ('Splitting size({}) is smaller than process ' +
                        'number({}), more processor would be ' +
                        'superflous').format(size, self.size)
            self._logger.warning(warn_msg)
            splited_sizes = [1]*size + [0]*(self.size - size)
        elif size % self.size != 0:
            residual = size % self.size
            splited_sizes = [size // self.size]*self.size
            for i in range(residual):
                splited_sizes[i] += 1
        else:
            splited_sizes = [size // self.size]*self.size

        return splited_sizes[self.rank]

    def merge_seq(self, seq):
        ''' Gather data in sub-process to root process.

        :param seq: Sub data sequence for current process
        :type seq: any Python object list

        :return: Merged data sequence from all processes in a communicator
        :rtype: any Python object list
        '''
        if self.size == 1:
            return seq

        mpi_comm = MPI.COMM_WORLD
        merged_seq= mpi_comm.allgather(seq)
        return list(chain(*merged_seq))


def master_only(func):
    ''' Decorator to limit a function to be called only in master process in MPI env.
    '''
    @wraps(func)
    def _call_in_master_proc(*args, **kwargs):
        if mpi.is_master:
            return func(*args, **kwargs)

    return _call_in_master_proc

