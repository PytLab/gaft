#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Roulette Wheel Selection implementation. '''

from random import random
from bisect import bisect_right
from itertools import accumulate

from ...plugin_interfaces.operators.selection import Selection

class RouletteWheelSelection(Selection):
    ''' Selection operator with fitness proportionate selection(FPS) or
    so-called roulette-wheel selection implementation.
    '''
    def __init__(self):
        pass

    def select(self, population, fitness):
        ''' Select a pair of parent using FPS algorithm.

        :param population: Population where the selection operation occurs.
        :type population: :obj:`gaft.components.Population`

        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`gaft.components.IndividualBase`
        '''
        # Normalize fitness values for all individuals.
        fit = population.all_fits(fitness)
        min_fit = min(fit)
        fit = [(i - min_fit) for i in fit]

        # Create roulette wheel.
        sum_fit = sum(fit)
        wheel = list(accumulate([i/sum_fit for i in fit]))

        # Select a father and a mother.
        father_idx = bisect_right(wheel, random())
        father = population[father_idx]
        mother_idx = (father_idx + 1) % len(wheel)
        mother = population[mother_idx]

        return father, mother

