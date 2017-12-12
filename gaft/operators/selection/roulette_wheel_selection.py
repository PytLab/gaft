#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Roulette Wheel Selection implementation. '''

from random import random
from bisect import bisect_right
from itertools import accumulate

from ...plugin_interfaces.operators.selection import Selection

class RouletteWheelSelection(Selection):
    def __init__(self):
        '''
        Selection operator with fitness proportionate selection(FPS) or
        so-called roulette-wheel selection implementation.
        '''
        pass

    def select(self, population, fitness):
        '''
        Select a pair of parent using FPS algorithm.
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

