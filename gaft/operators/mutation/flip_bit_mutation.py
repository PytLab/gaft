#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Flip Bit mutation implementation. '''

from random import random, uniform

from ...mpiutil import mpi
from ...plugin_interfaces.operators.mutation import Mutation
from ...components.binary_individual import BinaryIndividual
from ...components.decimal_individual import DecimalIndividual


class FlipBitMutation(Mutation):
    def __init__(self, pm):
        '''
        Mutation operator with Flip Bit mutation implementation.

        :param pm: The probability of mutation (usually between 0.001 ~ 0.1)
        :type pm: float in (0.0, 1.0]
        '''
        if pm <= 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')

        self.pm = pm

    def mutate(self, individual, engine):
        '''
        Mutate the individual.
        '''
        do_mutation = True if random() <= self.pm else False

        if do_mutation:
            for i, genome in enumerate(individual.chromsome):
                no_flip = True if random() > self.pm else False
                if no_flip:
                    continue

                if type(individual) is BinaryIndividual:
                    individual.chromsome[i] = genome^1
                elif type(individual) is DecimalIndividual:
                    a, b = individual.ranges[i]
                    eps = individual.precisions[i]
                    n_intervals = (b - a)//eps
                    n = int(uniform(0, n_intervals + 1))
                    individual.chromsome[i] = a + n*eps
                else:
                    raise TypeError('Wrong individual type: {}'.format(type(individual)))

            # Update solution.
            individual.solution = individual.decode()

        return individual


class FlipBitBigMutation(FlipBitMutation):
    def __init__(self, pm, pbm, alpha):
        '''
        Mutation operator using Flip Bit mutation implementation with adaptive
        big mutation rate to overcome premature or local-best solution.

        :param pm: The probability of mutation (usually between 0.001 ~ 0.1)
        :type pm: float in (0.0, 1.0]

        :param pbm: The probability of big mutation, usually more than 5 times
                    bigger than pm.
        :type pbm: float

        :param alpha: intensive factor
        :type alpha: float, in range (0.5, 1)
        '''
        super(self.__class__, self).__init__(pm)

        if not (0.0 < pbm < 1.0):
            raise ValueError('Invalid big mutation probability')
        if pbm < 5*pm and mpi.is_master:
            self.logger.warning('Relative low probability for big mutation')
        self.pbm = pbm

        # Intensive factor.
        if not (0.5 < alpha < 1.0):
            raise ValueError('Invalid intensive factor, should be in (0.5, 1.0)')
        self.alpha = alpha

    def mutate(self, individual, engine):
        '''
        Mutate the individual with adaptive big mutation rate.
        '''
        pm = self.pm

        if engine.fmax*self.alpha < engine.fmean:
            self.pm = self.pbm

        # Mutate with big probability.
        individual = super(self.__class__, self).mutate(individual, engine)

        # Recover probability.
        self.pm = pm

        return individual

