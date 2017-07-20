#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm selection operator class '''


class GASelection(object):
    '''
    Class for providing an interface to easily extend the behavior of selection
    operation.
    '''

    def __init__(self):
        '''
        The constructor of the base-class.
        '''
        pass

    def select(self, population, fitness):
        '''
        Called when we need to select parents from a population to later breeding.

        :param population: The current population.
        :type population: GAPopulation

        :return parents: Two selected individuals for crossover.
        :type parents: Tuple of tow GAIndividual objects.
        '''
        raise NotImplementedError

