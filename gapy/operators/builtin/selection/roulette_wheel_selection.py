#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Roulette Wheel Selection '''

from random import random
from bisect import bisect_right
from itertools import accumulate

from gapy.operators.selection import GASelection

class RouletteWheelSelection(GASelection):
    def __init__(self):
        '''
        Selection operator with fitness proportionate selection(FPS) or
        so-called roulette-wheel selection implementation.
        '''
        super(self.__class__, self).__init__()

    def select(self, population):
        '''
        Select a pair of parent using FPS algorithm.
        '''
        # Normalize fitness values for all individuals.
        fit = [population.fitness(indv) for indv in population.individuals]
        min_fit, max_fit = min(fit), max(fit)
        fit = list(accumulate([(i - min_fit)/(max_fit - min_fit) for i in fit]))

        # Select a father and a mother.
        father_idx = bisect_right(fit, random())
        father = population[father_idx]
        mother_idx = (father_idx + 1) % len(fit)
        mother = population[mother_idx]

        return father, mother

