#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm crossover operator class '''

class CrossoverMeta(type):
    '''
    Metaclass for crossover operator class.
    '''
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, attrs):
        if 'cross' not in attrs:
            raise AttributeError('crossover operator class must have cross method')

        if 'pc' in attrs and (attrs['pc'] <= 0.0 or attrs['pc'] > 1.0):
            raise ValueError('Invalid crossover probability')

        return type.__new__(cls, name, bases, attrs)


class GACrossover(metaclass=CrossoverMeta):
    '''
    Class for providing an interface to easily extend the behavior of crossover
    operation between two individuals for children breeding.
    '''

    pc = 0.8

    def __init__(self, pc):
        '''
        The constructor of the base-class.

        :param pc: The probability of crossover (usaully between 0.25 ~ 1.0)
        :type pc: float in (0.0, 1.0]
        '''
        if pc <= 0.0 or pc > 1.0:
            raise ValueError('Invalid crossover probability')
        self.pc = pc

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

