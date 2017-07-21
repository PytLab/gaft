#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random

from ...plugin_interfaces.operators.mutation import GAMutation


class FlipBitMutation(GAMutation):
    def __init__(self, pm):
        '''
        Mutation operator with Flip Bit mutation implementation.

        :param pm: The probability of mutation (usually between 0.001 ~ 0.1)
        :type pm: float in (0.0, 1.0]
        '''
        super(self.__class__, self).__init__(pm=pm)

    def mutate(self, individual):
        '''
        Mutate the individual.
        '''
        do_mutation = True if random() <= self.pm else False

        if do_mutation:
            for i, genome in enumerate(individual.chromsome):
                do_flip = True if random() <= self.pm else False
                if do_flip:
                    individual.chromsome[i] ^= 1

            # Update variants.
            individual.variants = individual.decode()

        return individual

