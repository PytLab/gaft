#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log2
from itertools import accumulate

class GAIndividual(object):
    def __init__(self, variants, ranges, encoding='binary', eps=None):
        '''
        Class for individual in population.

        :param variants: the variable vector of the target function.
        :type variants: list of float.

        :param ranges: value ranges for all entries in variants.
        :type ranges: list of range tuples. e.g. [(0, 1), (-1, 1)]

        :param encoding: gene encoding, 'decimal' or 'binary', default is 'binary'.
        :param eps: decrete precision for binary encoding, default is 0.01.
        '''
        self._check_parameters()

        self.variants = variants
        self.ranges = ranges
        self.eps = 0.01 if encoding == 'binary' and eps is None else eps
        self.encoding = encoding

        self.lengths = [int(log2((b-a)/self.eps) + 1) for a, b in ranges]
        self.gene_indices = self._get_gene_indices()
        self.chromsome = self.encode()

    def _check_parameters(self):
        # Need implementation.
        pass

    def encode(self, variants=None, encoding=None):
        '''
        Encode variant to gene sequence in individual using different encoding.

        :param variants: the variable vector of the target function.
        :type variants: list of float.

        :param encoding: gene encoding, 'binary' or 'decimal',
                         default is the same with that of individual.
        '''
        variants = self.variants if variants is None else variants
        encoding = self.encoding if encoding is None else encoding

        if encoding == 'decimal':
            return variants

        chromsome = []
        for var, (a, _), length in zip(variants, self.ranges, self.lengths):
            chromsome.extend(self.binarize(var-a, self.eps, length))

        return chromsome

    def decode(self, chromsome=None, encoding=None):
        ''' 
        Decode gene sequence to variants of target function.

        :param chromsome: chromsome (gene sequence).
        :type chromsome: list of int/float

        :param encoding: gene encoding, 'binary' or 'decimal',
                         default is the same with that of individual.
        '''
        chromsome = self.chromsome if chromsome is None else chromsome
        encoding = self.encoding if encoding is None else encoding

        if encoding == 'decimal':
            return self.variants

        return [self.decimalize(self.chromsome[start: end], self.eps, lower_bound)
                for (start, end), (lower_bound, _) in zip(self.gene_indices, self.ranges)]

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

