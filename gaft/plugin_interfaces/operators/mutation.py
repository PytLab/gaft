#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm mutation operator class '''

from ..metaclasses import MutationMeta


class GAMutation(metaclass=MutationMeta):
    '''
    Class for providing an interface to easily extend the behavior of selection
    operation.
    '''
    # Default mutation probability.
    pm = 0.1

    def mutate(self, individual):
        '''
        Called when an individual to be mutated.

        :param individual: The individual to be mutated.
        :type individual: GAInvidual
        '''
        raise NotImplementedError

