#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Tournament Selection implementation. '''

from random import sample

from ...plugin_interfaces.operators.selection import Selection


class TournamentSelection(Selection):
    ''' Selection operator using Tournament Strategy with tournament size equals
    to two by default.

    :param tournament_size: Individual number in one tournament
    :type tournament_size: int
    '''
    def __init__(self, tournament_size=2):
        self.tournament_size = tournament_size

    def select(self, population, fitness):
        ''' Select a pair of parent using Tournament strategy.

        :param population: Population where the selection operation occurs.
        :type population: :obj:`gaft.components.Population`

        :return: Selected parents (a father and a mother)
        :rtype: list of :obj:`gaft.components.IndividualBase`
        '''
        # Competition function.
        all_fits = population.all_fits(fitness)
        def complete(competitors):
            '''
            Competition function.
            '''
            key = lambda indv: all_fits[population.individuals.index(indv)]
            return max(competitors, key=key)

        # Check validity of tournament size.
        if self.tournament_size >= len(population):
            msg = 'Tournament size({}) is larger than population size({})'
            raise ValueError(msg.format(self.tournament_size, len(population)))

        # Pick winners of two groups as parent.
        competitors_1 = sample(population.individuals, self.tournament_size)
        competitors_2 = sample(population.individuals, self.tournament_size)
        father, mother = complete(competitors_1), complete(competitors_2)

        return father, mother

