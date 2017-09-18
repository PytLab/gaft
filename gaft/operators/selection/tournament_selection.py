#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Tournament Selection '''

from random import sample

from ...plugin_interfaces.operators.selection import GASelection


class TournamentSelection(GASelection):
    def __init__(self, tournament_size=2):
        '''
        Selection operator using Tournament Strategy with tournament size equals
        to two by default.
        '''
        self.tournament_size = tournament_size

    def select(self, population, fitness):
        '''
        Select a pair of parent using Tournament strategy.
        '''
        # Competition function.
        complete = lambda competitors: max(competitors, key=fitness)

        # Check validity of tournament size.
        if self.tournament_size >= len(population):
            msg = 'Tournament size({}) is larger than population size({})'
            raise ValueError(msg.format(self.tournament_size, len(population)))

        # Pick winners of two groups as parent.
        competitors_1 = sample(population.individuals, self.tournament_size)
        competitors_2 = sample(population.individuals, self.tournament_size)
        father, mother = complete(competitors_1), complete(competitors_2)

        return father, mother

