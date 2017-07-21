#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .individual import GAIndividual


class GAPopulation(object):
    def __init__(self, indv_template, size=100):
        '''
        Class for representing population in genetic algorithm.

        :param indv_template: A template individual to clone all the other
                              individuals in current population.

        :param size: The size of population, number of individuals in population.
        :type size: int

        '''
        # Population size.
        self.size = size

        # Template individual.
        self.indv_template = indv_template

        # All individuals.
        self.individuals = []

    def init(self):
        '''
        Initialize current population with individuals.
        '''
        for i in range(self.size):
            indv = GAIndividual(ranges=self.indv_template.ranges,
                                encoding=self.indv_template.encoding,
                                eps=self.indv_template.eps)
            self.individuals.append(indv)

    def new(self):
        '''
        Create a new emtpy population.
        '''
        return self.__class__(indv_template=self.indv_template,
                              size=self.size)

    def __getitem__(self, key):
        '''
        Get individual by index.
        '''
        if key < 0 or key >= self.size:
            raise IndexError('Individual index out of range')
        return self.individuals[key]

    def best_indv(self, fitness):
        '''
        The individual with the best fitness.

        '''
        return max(self.individuals, key=fitness)

