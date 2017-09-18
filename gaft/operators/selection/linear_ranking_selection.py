#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Linear Ranking Selection implementation. '''

from random import random
from itertools import accumulate
from bisect import bisect_right

from ...plugin_interfaces.operators.selection import GASelection


class LinearRankingSelection(GASelection):
    def __init__(self, pmin=0.1, pmax=0.9):
        '''
        Selection operator using Linear Ranking selection method.

        Reference: Baker J E. Adaptive selection methods for genetic
        algorithms[C]//Proceedings of an International Conference on Genetic
        Algorithms and their applications. 1985: 101-111.
        '''
        # Selection probabilities for the worst and best individuals.
        self.pmin, self.pmax = pmin, pmax

    def select(self, population, fitness):
        '''
        Select a pair of parent individuals using linear ranking method.
        '''
        # Individual number.
        NP = len(population)

        # Add rank to all individuals in population.
        sorted_indvs = sorted(population.individuals, key=fitness, reverse=True)

        # Assign selection probabilities linearly.
        p = lambda i: (self.pmin + (self.pmax - self.pmin)*(i)/(NP-1))
        probabilities = [self.pmin] + [p(i) for i in range(1, NP-1)] + [self.pmax]

        # Normalize probabilities.
        psum = sum(probabilities)
        wheel = list(accumulate([p/psum for p in probabilities]))

        # Select parents.
        father_idx = bisect_right(wheel, random())
        father = population[father_idx]
        mother_idx = (father_idx + 1) % len(wheel)
        mother = population[mother_idx]

        return father, mother

