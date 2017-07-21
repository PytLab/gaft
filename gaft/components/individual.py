#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log2
from itertools import accumulate
from random import uniform


class GAIndividual(object):
    def __init__(self, ranges, encoding='binary', eps=0.001):
        '''
        Class for individual in population.

        :param ranges: value ranges for all entries in variants.
        :type ranges: list of range tuples. e.g. [(0, 1), (-1, 1)]

        :param encoding: gene encoding, 'decimal' or 'binary', default is binary.
        :param eps: decrete precision for binary encoding, default is 0.001.

        '''
        self._check_parameters()

        self.ranges = ranges
        self.eps = eps
        self.encoding = encoding

        # Lengths for all binary sequence in chromsome.
        self.lengths = [int(log2((b-a)/eps)) for a, b in ranges]

        # Correct decrete precision according to binary sequence length.
        self.precisions = [(b - a)/(2**l - 1) for l, (a, b) in zip(self.lengths, self.ranges)]

        # The start and end indices for each gene segment for entries in variants.
        self.gene_indices = self._get_gene_indices()

        # Generate randomly.
        self.variants = self._init_variants()

        # Gene encoding.
        self.chromsome = self.encode()

    def init(self, chromsome=None, variants=None):
        '''
        Initialize the individual by providing chromsome or variants.
        If both chromsome and variants are provided, only the chromsome would
        be used.

        :param chromsome: chromesome sequence for the individual
        :type chromsome: list of float/int.

        :param variants: the variable vector of the target function.
        :type variants: list of float.
        '''
        if not any([chromsome, variants]):
            msg = 'Chromsome or variants must be supplied for individual initialization'
            raise ValueError(msg)

        if chromsome:
            self.chromsome = chromsome
            self.variants = self.decode()
        else:
            self.variants = variants
            self.chromsome = self.encode()

        return self

    def clone(self):
        '''
        Clone a new individual from current one.
        '''
        indv = self.__class__(self.ranges, encoding=self.encoding, eps=self.eps)
        indv.init(chromsome=self.chromsome)
        return indv

    def _check_parameters(self):
        # Need implementation.
        pass

    def _init_variants(self):
        '''
        Initialize individual variants randomly.
        '''
        return [uniform(a, b) for a, b in self.ranges]

    def encode(self):
        '''
        Encode variant to gene sequence in individual using different encoding.
        '''
        if self.encoding == 'decimal':
            return self.variants

        chromsome = []
        for var, (a, _), length, eps in zip(self.variants, self.ranges,
                                            self.lengths, self.precisions):
            chromsome.extend(self.binarize(var-a, eps, length))

        return chromsome

    def decode(self):
        ''' 
        Decode gene sequence to variants of target function.
        '''
        if self.encoding == 'decimal':
            return self.variants

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

