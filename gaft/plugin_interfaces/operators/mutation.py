#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for Genetic Algorithm mutation operator class '''

from ..metaclasses import MutationMeta


class Mutation(metaclass=MutationMeta):
    ''' Class for providing an interface to easily extend the behavior of selection
    operation.

    Attributes:

        pm(float): Default mutation probability, default is 0.1
    '''
    # Default mutation probability.
    pm = 0.1

    def mutate(self, individual, engine):
        ''' Called when an individual to be mutated.

        :param individual: The individual to be mutated
        :type individual: gaft.components.IndividualBase

        :param engine: The GA engine where the mutation operator belongs.
        :type engine: gaft.engine.GAEngine
        '''
        raise NotImplementedError

