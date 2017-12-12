#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm mutation operator class '''

from ..metaclasses import MutationMeta


class Mutation(metaclass=MutationMeta):
    '''
    Class for providing an interface to easily extend the behavior of selection
    operation.
    '''
    # Default mutation probability.
    pm = 0.1

    def mutate(self, individual, engine):
        '''
        Called when an individual to be mutated.

        :param individual: The individual to be mutated.
        :type individual: subclass of IndvidualBase

        :param engine: The GA engine where the mutation operator belongs.
        :type engine: GAEngine
        '''
        raise NotImplementedError

