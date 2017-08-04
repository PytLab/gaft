#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Genetic Algorithm engine definition '''

import logging

from .plugin_interfaces.analysis import OnTheFlyAnalysis
from .mpiutil import mpi


class GAEngine(object):
    '''
    Class for representing a Genetic Algorithm engine.
    '''
    def __init__(self, population, selection, crossover, mutation,
                 fitness=None, analysis=None):
        '''
        The Genetic Algorithm engine class is the central object in GAPY framework
        for running a genetic algorithm optimization. Once the population with
        individuals,  a set of genetic operators and fitness function are setup,
        the engine object unites these informations and provide means for running
        a genetic algorthm optimization.

        :param population: The GAPopulation to be reproduced in evolution iteration.
        :param selection: The GASelection to be used for individual seleciton.
        :param crossover: The GACrossover to be used for individual crossover.
        :param mutation: The GAMutation to be used for individual mutation.
        :param fitness: The fitness calculation function for an individual in population.

        :param analysis: All analysis class for on-the-fly analysis.
        :type analysis: list of OnTheFlyAnalysis subclasses.
        '''
        # Check parameters validity.
        self._check_parameters()

        # Set logger.
        logger_name = 'gaft.{}'.format(self.__class__.__name__)
        self.logger = logging.getLogger(logger_name)

        # Attributes assignment.
        self.population = population
        self.fitness = fitness
        self.selection= selection
        self.crossover= crossover
        self.mutation= mutation

        self.analysis = [] if analysis is None else [a() for a in analysis]

    def run(self, ng=100):
        '''
        Run the Genetic Algorithm optimization iteration with specified parameters.

        :param control_parameters: An instance of GAControlParamters specifying
                                   number of evolution generations etc.
        '''
        if self.fitness is None:
            raise AttributeError('No fitness function in GA engine')

        # Setup analysis objects.
        for a in self.analysis:
            a.setup(ng=ng, engine=self)

        # Enter evolution iteration.
        for g in range(ng):
            # Scatter jobs to all processes.
            local_indvs = []
            local_size = mpi.split_size(self.population.size // 2)

            # Fill the new population.
            for _ in range(local_size):
                # Select father and mother.
                parents = self.selection.select(self.population, fitness=self.fitness)
                # Crossover.
                children = self.crossover.cross(*parents)
                # Mutation.
                children = [self.mutation.mutate(child) for child in children]
                # Collect children.
                local_indvs.extend(children)

            # Gather individuals from all processes.
            indvs = mpi.merge_seq(local_indvs)
            # The next generation.
            self.population.individuals = indvs

            # Run all analysis if needed.
            for a in self.analysis:
                if g % a.interval == 0:
                    a.register_step(g=g, population=self.population, engine=self)

        # Perform the analysis post processing.
        for a in self.analysis:
            a.finalize(population=self.population, engine=self)

    def _check_parameters(self):
        '''
        Helper function to check parameters of engine.
        '''
        # Need implementation.
        pass

    # Decorators.

    def fitness_register(self, fn):
        '''
        A decorator for fitness function register.
        '''
        self.fitness = fn

    def analysis_register(self, analysis_cls):
        '''
        A decorator for analysis regsiter.
        '''
        if not issubclass(analysis_cls, OnTheFlyAnalysis):
            raise TypeError('analysis class must be subclass of OnTheFlyAnalysis')

        # Add analysis instance to engine.
        analysis = analysis_cls()
        self.analysis.append(analysis)

