#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gapy.components.individual import GAIndividual


class GAPopulation(object):
    def __init__(self, indv_template, fitness, size=100):
        '''
        Class for representing population in genetic algorithm.

        :param indv_template: A template individual to clone all the other
                              individuals in current population.

        :param fitness: fitness function for individual.
        :type fitness: callable object.

        :param size: The size of population, number of individuals in population.
        :type size: int

        '''
        # Population size.
        self.size = size

        # Template individual.
        self.indv_template = indv_template

        # Fitness function.
        self.fitness = fitness

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
                              fitness=self.fitness,
                              size=self.size)

    def __getitem__(self, key):
        '''
        Get individual by index.
        '''
        if key < 0 or key >= self.size:
            raise IndexError('Individual index out of range')
        return self.individuals[key]

    @property
    def best_indv(self):
        '''
        The individual with the best fitness.

        '''
        return max(self.individuals, key=self.fitness)

