#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Genetic Algorithm engine definition '''

import logging

from .plugin_interfaces.analysis import OnTheFlyAnalysis


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
        self._set_logger()

        # Attributes assignment.
        self.population = population
        self.fitness = fitness
        self.selection= selection
        self.crossover= crossover
        self.mutation= mutation

        self.analysis = [] if analysis is None else [a() for a in analysis]

    def _set_logger(self):
        '''
        Helper function to set logger for engine.
        '''
        logger = logging.getLogger('GAEngine')
        logger.setLevel(logging.INFO)
        console_hdlr = logging.StreamHandler()
        console_hdlr.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)s   %(levelname)-8s %(message)s')
        console_hdlr.setFormatter(formatter)
        logger.addHandler(console_hdlr)

        self.logger = logger

    def run(self, ng=100):
        '''
        Run the Genetic Algorithm optimization iteration with specified parameters.

        :param control_parameters: An instance of GAControlParamters specifying
                                   number of evolution generations etc.
        '''
        if self.fitness is None:
            raise AttributeError('No fitness function in GA engine')

        # Initialize a population.
        self.population.init()

        # Setup analysis objects.
        for a in self.analysis:
            a.setup(self.population, self)

        # Enter evolution iteration.
        for g in range(ng):
            # Next generation population.
            new_population = self.population.new()

            # Fill the new population.
            for i in range(0, new_population.size, 2):
                # Select father and mother.
                parents = self.selection.select(self.population, fitness=self.fitness)
                # Crossover.
                children = self.crossover.cross(*parents)
                # Mutation.
                children = [self.mutation.mutate(child) for child in children]
                # Add to population.
                new_population.individuals.extend(children)

            self.population = new_population

            # Run all analysis if needed.
            for a in self.analysis:
                if g % a.interval == 0:
                    a.register_step(ng=g, population=new_population, engine=self)

        # Perform the analysis post processing.
        for a in self.analysis:
            a.finalize(population=self.population, engine=self)

    def _check_parameters(self):
        '''
        Helper function to check parameters of engine.
        '''
        pass

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

