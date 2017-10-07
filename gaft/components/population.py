#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .individual import GAIndividual


class Memoized(object):
    '''
    Descriptor for population statistical varibles caching.
    '''
    def __init__(self, func):
        self.func = func
        self.result = None

    def __get__(self, instance, cls):
        self.instance = instance
        return self

    def __call__(self, fitness):
        if self.instance._updated:
            # Update and memoize result.
            self.result = self.func(self.instance, fitness)
            # Recover flag.
            self.instance._updated = False
        return self.result


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
        if size % 2 != 0:
            raise ValueError('Population size must be an even number')
        self.size = size

        # Template individual.
        self.indv_template = indv_template

        # All individuals.
        self.individuals = []

        # Flag for monitoring changes of population.
        self._updated = False

    def init(self, indvs=None):
        '''
        Initialize current population with individuals.

        :param indvs: Initial individuals in population, randomly initialized
                      individuals are created if not provided.
        :type indvs: list of GAIndividual
        '''
        if indvs is None:
            for _ in range(self.size):
                indv = GAIndividual(ranges=self.indv_template.ranges,
                                    encoding=self.indv_template.encoding,
                                    eps=self.indv_template.eps)
                self.individuals.append(indv)
        else:
            # Check individuals.
            if len(indvs) != self.size:
                raise ValueError('Invalid individuals number')
            for indv in indvs:
                if not isinstance(indv, GAIndividual):
                    raise ValueError('individual must be GAIndividual object')
            self.individuals = indvs

        self.flag_update()

        return self

    def flag_update(self):
        '''
        Update individual update flag to True.
        '''
        self._updated = True

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
            raise IndexError('Individual index({}) out of range'.format(key))
        return self.individuals[key]

    def __len__(self):
        '''
        Get length of population.
        '''
        return len(self.individuals)

    def best_indv(self, fitness):
        '''
        The individual with the best fitness.

        '''
        all_fits = self.all_fits(fitness)
        return max(self.individuals,
                   key=lambda indv: all_fits[self.individuals.index(indv)])

    def worst_indv(self, fitness):
        '''
        The individual with the worst fitness.
        '''
        all_fits = self.all_fits(fitness)
        return min(self.individuals,
                   key=lambda indv: all_fits[self.individuals.index(indv)])

    def max(self, fitness):
        '''
        Get the maximum fitness value in population.
        '''
        return fitness(self.best_indv(fitness))

    def min(self, fitness):
        '''
        Get the minimum value of fitness in population.
        '''
        return fitness(self.worst_indv(fitness))

    def mean(self, fitness):
        '''
        Get the average fitness value in population.
        '''
        all_fits = self.all_fits(fitness)
        return sum(all_fits)/len(all_fits)

    @Memoized
    def all_fits(self, fitness):
        '''
        Get all fitness values in population.
        '''
        return [fitness(indv) for indv in self.individuals]

