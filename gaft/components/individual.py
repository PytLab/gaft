#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log2
from itertools import accumulate
from random import uniform
import logging

from ..mpiutil import mpi


class SolutionRanges(object):
    ''' Descriptor for solution ranges.
    '''
    def __init__(self):
        self.__ranges = []

    def __get__(self, obj, owner):
        return self.__ranges

    def __set__(self, obj, ranges):
        # Check.
        if type(ranges) not in [tuple, list]:
            raise TypeError('solution ranges must be a list of range tuples')
        for rng in ranges:
            if type(rng) not in [tuple, list]:
                raise TypeError('range({}) is not a tuple containing two numbers'.format(rng))
            if len(rng) != 2:
                raise ValueError('length of range({}) not equal to 2')
            a, b = rng
            if a >= b:
                raise ValueError('Wrong range value {}'.format(rng))
        # Assignment.
        self.__ranges = ranges


class DecretePrecision(object):
    ''' Descriptor for individual decrete precisions.
    '''
    def __init__(self):
        self.__precisions = []

    def __get__(self, obj, owner):
        return self.__precisions

    def __set__(self, obj, precisions):
        if type(precisions) is float:
            self.__precisions = [precisions]*len(obj.ranges)
        else:
            # Check.
            if len(precisions) != len(obj.ranges):
                raise ValueError('Lengths of eps and ranges should be the same')
            for (a, b), eps in zip(obj.ranges, precisions):
                if eps > (b - a):
                    msg = 'Invalid precision {} in range ({}, {})'.format(eps, a, b)
                    raise ValueError(msg)
            self.__precisions = precisions


class IndividualBase(object):
    ''' Base class for individuals.
    '''
    # Solution ranges.
    ranges = SolutionRanges()

    # Original decrete precisions (provided by users).
    eps = DecretePrecision()
    
    # Actual decrete precisions used in GA.
    precisions = DecretePrecision()

    def __init__(self, ranges, eps=0.001):
        self.ranges = ranges
        self.eps = eps
        self.precisions = eps

        self.variants, self.chromsome = [], []

    def _rand_variants(self):
        ''' Initialize individual variants randomly.
        '''
        variants = []
        for eps, (a, b) in zip(self.precisions, self.ranges):
            n_intervals = (b - a)//eps
            n = int(uniform(0, n_intervals + 1))
            variants.append(a + n*eps)
        return variants

    def init(self, chromsome=None, variants=None):
        '''
        Initialize the individual by providing chromsome or variants.

        If both chromsome and variants are provided, only the chromsome would
        be used. If neither is provided, individual would be initialized randomly.

        :param chromsome: chromesome sequence for the individual
        :type chromsome: list of float/int.

        :param variants: the variable vector of the target function.
        :type variants: list of float.
        '''
        if not any([chromsome, variants]):
            self.variants = self._rand_variants()
            self.chromsome = self.encode()
        elif chromsome:
            self.chromsome = chromsome
            self.variants = self.decode()
        else:
            self.variants = variants
            self.chromsome = self.encode()

        return self

    def encode(self):
        ''' *NEED IMPLIMENTATION*
        Convert variants to chromsome sequence.
        '''
        raise NotImplementedError

    def decode(self):
        ''' *NEED IMPLIMENTATION*
        Convert chromsome sequence to variants.
        '''
        raise NotImplementedError


class BinaryIndividual(IndividualBase):
    def __init__(self, ranges, eps=0.001, verbosity=1):
        '''
        Class for individual in population. Random variants will be initialized
        by default.

        NOTE: The decrete precisions for different components in varants may be
              adjusted automatically (possible precision loss) if eps and ranges
              are not appropriate.
              
              Please check it before you put it into GA engine. If you don't want
              to see the warning info, set verbosity to 0 :)

        :param ranges: value ranges for all entries in variants.
        :type ranges: list of range tuples. e.g. [(0, 1), (-1, 1)]

        :param eps: decrete precisions for binary encoding, default is 0.001.
        :type eps: float or float list with the same length with ranges.

        :param verbosity: The verbosity level of info output.
        :param verbosity: int, 0 or 1(default)
        '''
        super(self.__class__, self).__init__(ranges, eps)

        self.verbosity = verbosity

        # Lengths for all binary sequence in chromsome and adjusted decrete precisions.
        self.lengths = []

        for i, ((a, b), eps) in enumerate(zip(self.ranges, self.eps)):
            length = int(log2((b - a)/eps))
            precision = (b - a)/(2**length)

            if precision != eps and mpi.is_master and self.verbosity:
                print('Precision loss {} -> {}'.format(eps, precision))

            self.lengths.append(length)
            self.precisions[i] = precision

        # The start and end indices for each gene segment for entries in variants.
        self.gene_indices = self._get_gene_indices()

        # Initialize individual randomly.
        self.init()

    def clone(self):
        '''
        Clone a new individual from current one.
        '''
        indv = self.__class__(self.ranges,
                              eps=self.eps,
                              verbosity=self.verbosity)
        indv.init(chromsome=self.chromsome)
        return indv

    def encode(self):
        '''
        Encode variant to gene sequence in individual using different encoding.
        '''
        chromsome = []
        for var, (a, _), length, eps in zip(self.variants, self.ranges,
                                            self.lengths, self.precisions):
            chromsome.extend(self.binarize(var-a, eps, length))

        return chromsome

    def decode(self):
        ''' 
        Decode gene sequence to variants of target function.
        '''
        variants =  [self.decimalize(self.chromsome[start: end], eps, lower_bound)
                     for (start, end), (lower_bound, _), eps in
                     zip(self.gene_indices, self.ranges, self.precisions)]
        return variants

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

