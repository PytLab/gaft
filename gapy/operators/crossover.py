#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm crossover operator class '''


class GACrossover(object):
    '''
    Class for providing an interface to easily extend the behavior of crossover
    operation between two individuals.
    '''
    def __init__(self):
        '''
        The constructor of the base-class.
        '''
        pass

    def cross(self, father, mother):
        '''
        Called when we need to cross parents to generate children.

        :param father: The parent individual to be crossed.
        :type father: GAIndividual

        :param mother: The parent individual to be crossed.
        :type mother: GAIndividual

        :return children: Two new children individuals.
        :type children: Tuple of two GAIndividual objects.
        '''
        raise NotImplementedError

