#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm selection operator class '''

class SelectionMeta(type):
    '''
    Metaclass for selection operator class.
    '''
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, attrs):
        if 'select' not in attrs:
            raise AttributeError('selection operator class must have select method')

        return type.__new__(cls, name, bases, attrs)


class GASelection(metaclass=SelectionMeta):
    '''
    Class for providing an interface to easily extend the behavior of selection
    operation.
    '''

    def select(self, population, fitness):
        '''
        Called when we need to select parents from a population to later breeding.

        :param population: The current population.
        :type population: GAPopulation

        :return parents: Two selected individuals for crossover.
        :type parents: Tuple of tow GAIndividual objects.
        '''
        raise NotImplementedError

