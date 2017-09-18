#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Exponential Ranking Selection implemention. '''

from random import random
from itertools import accumulate
from bisect import bisect_right

from ...plugin_interfaces.operators.selection import GASelection


class ExponentialRankingSelection(GASelection): 
    def __init__(self, base=0.5):
        '''
        Selection operator using Exponential Ranking selection method.

        :param base: The base of exponent
        :type base: float in range (0.0, 1.0)
        '''
        if not (0.0 < base < 1.0):
            raise ValueError('The base of exponent c must in range (0.0, 1.0)')

        self.base = base

    def select(self, population, fitness):
        '''
        Select a pair of parent individuals using exponential ranking method.
        '''
        # Individual number.
        NP = len(population)

        # NOTE: Here the rank i belongs to {1, ..., N}
        p = lambda i: self.base**(NP - i)
        probabilities = [p(i) for i in range(1, NP + 1)]

        # Normalize probabilities.
        psum = sum(probabilities)
        wheel = list(accumulate([p/psum for p in probabilities]))

        # Select parents.
        father_idx = bisect_right(wheel, random())
        father = population[father_idx]
        mother_idx = (father_idx + 1) % len(wheel)
        mother = population[mother_idx]

        return father, mother

