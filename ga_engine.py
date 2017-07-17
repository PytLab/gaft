#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Genetic Algorithm engine definition '''

class GAEngine(object):
    '''
    Class for representing a Genetic Algorithm engine.
    '''
    def __init__(self,
                 population,
                 fitness,
                 selection,
                 crossover,
                 mutation):
        '''
        The Genetic Algorithm engine class is the central object in GAPY framework
        for running a genetic algorithm optimization. Once the population with
        individuals,  a set of genetic operators and fitness function are setup,
        the engine object unites these informations and provide means for running
        a genetic algorthm optimization.

        :param population: The GAPopulation to be reproduced in evolution iteration.
        :param fitness: The fitness calculation function for an individual in population.
        '''
        # Check parameters validity.
        self._check_parameters()

        # Attributes assignment.
        self.fitness = fitness
        self.selection= selection
        self.crossover= crossover
        self.mutation= mutation

    def run(self, control_parameters):
        '''
        Run the Genetic Algorithm optimization iteration with specified parameters.

        :param control_parameters: An instance of GAControlParamters specifying
                                   number of evolution generations etc.
        '''
        # Initialize a population.
        self.population.init()

        # Enter evolution iteration.
        for g in range(control_parameters.generation_number):
            # Next generation population.
            new_population = self.population.clone()

            # Fill the new population.
            for i in range(0, new_population.size, 2):
                # Select father and mother.
                parents = self.selection.select(self.population)
                # Crossover.
                children = self.crossover.cross(parents)
                # Mutation.
                children = [self.mutation.mutate(child) for child in children]
                # Add to population.
                new_population[i], new_population[i+1] = children

            self.population = new_population

    def _check_parameters():
        '''
        Helper function to check parameters of engine.
        '''
        pass

