#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Individual with binary encoding.
'''
from math import log2
from itertools import accumulate
import logging

from .individual import IndividualBase
from ..mpiutil import mpi


class BinaryIndividual(IndividualBase):
    def __init__(self, ranges, eps=0.001):
        '''
        Class for individual in population. Random solution will be initialized
        by default.

        NOTE: The decrete precisions for different components in varants may be
              adjusted automatically (possible precision loss) if eps and ranges
              are not appropriate.

        :param ranges: value ranges for all entries in solution.
        :type ranges: list of range tuples. e.g. [(0, 1), (-1, 1)]

        :param eps: decrete precisions for binary encoding, default is 0.001.
        :type eps: float or float list with the same length with ranges.
        '''
        super(self.__class__, self).__init__(ranges, eps)

        # Lengths for all binary sequence in chromsome and adjusted decrete precisions.
        self.lengths = []

        for i, ((a, b), eps) in enumerate(zip(self.ranges, self.eps)):
            length = int(log2((b - a)/eps))
            precision = (b - a)/(2**length)
            self.lengths.append(length)
            self.precisions[i] = precision

        # The start and end indices for each gene segment for entries in solution.
        self.gene_indices = self._get_gene_indices()

        # Initialize individual randomly.
        self.init()

    def encode(self):
        '''
        Encode solution to gene sequence in individual using different encoding.
        '''
        chromsome = []
        for var, (a, _), length, eps in zip(self.solution, self.ranges,
                                            self.lengths, self.precisions):
            chromsome.extend(self.binarize(var-a, eps, length))

        return chromsome

    def decode(self):
        ''' 
        Decode gene sequence to solution of target function.
        '''
        solution =  [self.decimalize(self.chromsome[start: end], eps, lower_bound)
                     for (start, end), (lower_bound, _), eps in
                     zip(self.gene_indices, self.ranges, self.precisions)]
        return solution

    def _get_gene_indices(self):
        '''
        Helper function to get gene slice indices.
        '''
        end_indices = list(accumulate(self.lengths))
        start_indices = [0] + end_indices[: -1]
        return list(zip(start_indices, end_indices))

    @staticmethod
    def binarize(decimal, eps, length):
        '''
        Helper function to convert a float to binary sequence.

        :param decimal: the decimal number to be converted.
        :param eps: the decrete precision of binary sequence.
        :param length: the length of binary sequence.
        '''
        n = int(decimal/eps)
        bin_str = '{:0>{}b}'.format(n, length)
        return [int(i) for i in bin_str]

    @staticmethod
    def decimalize(binary, eps, lower_bound):
        '''
        Helper function to convert a binary sequence back to decimal number.
        '''
        bin_str = ''.join([str(bit) for bit in binary])
        return lower_bound + int(bin_str, 2)*eps

