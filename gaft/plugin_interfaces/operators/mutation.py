#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm mutation operator class '''

class MutationMeta(type):
    '''
    Metaclass for mutation operator class.
    '''
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, attrs):
        if 'mutate' not in attrs:
            raise AttributeError('mutation operator class must have mutate method')

        if 'pm' in attrs and (attrs['pm'] <= 0.0 or attrs['pm'] > 1.0):
            raise ValueError('Invalid mutation probability')

        return type.__new__(cls, name, bases, attrs)


class GAMutation(metaclass=MutationMeta):
    '''
    Class for providing an interface to easily extend the behavior of selection
    operation.
    '''

    # Default mutation probability.
    pm = 0.1

    def __init__(self, pm):
        '''
        The constructor of the base-class.

        :param pm: The probability of mutation (usually between 0.001 ~ 0.1)
        :type pm: float in (0.0, 1.0]
        '''
        if pm <= 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')

        self.pm = pm

    def mutate(self, individual):
        '''
        Called when an individual to be mutated.

        :param individual: The individual to be mutated.
        :type individual: GAInvidual
        '''
        raise NotImplementedError

