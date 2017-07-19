#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm selection operator class '''


class GASelection(object):
    '''
    Class for providing an interface to easily extend the behavior of selection
    operation.
    '''

    def __init__(self, fitness):
        '''
        The constructor of the base-class.
        '''
        self.fitness = fitness

    def select(self, population):
        '''
        Called when we need to select parents from a population.

        :param population: The current population.
        :type population: GAPopulation

        :return parents: Two selected individuals for crossover.
        :type parents: Tuple of tow GAIndividual objects.
        '''
        raise NotImplementedError

