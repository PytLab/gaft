#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for engine run.
'''

import unittest
from math import sin, cos

from gaft import GAEngine
from gaft.components import BinaryIndividual, DecimalIndividual
from gaft.components import Population
from gaft.operators import RouletteWheelSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation


class GAEngineTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_binary_run(self):
        '''
        Make sure GA engine can run correctly.
        '''
        indv_template = BinaryIndividual(ranges=[(0, 10)], eps=0.001)
        population = Population(indv_template=indv_template, size=50).init()

        # Create genetic operators.
        selection = RouletteWheelSelection()
        crossover = UniformCrossover(pc=0.8, pe=0.5)
        mutation = FlipBitMutation(pm=0.1)

        # Create genetic algorithm engine.
        engine = GAEngine(population=population, selection=selection,
                          crossover=crossover, mutation=mutation)

        @engine.fitness_register
        @engine.minimize
        def fitness(indv):
            x, = indv.solution
            return x + 10*sin(5*x) + 7*cos(4*x)

        engine.run(50)

    def test_decimal_run(self):
        '''
        Make sure GA engine can run correctly with decimal encoding individuals.
        '''
        indv_template = DecimalIndividual(ranges=[(0, 10)], eps=0.001)
        population = Population(indv_template=indv_template, size=50).init()

        # Create genetic operators.
        selection = RouletteWheelSelection()
        crossover = UniformCrossover(pc=0.8, pe=0.5)
        mutation = FlipBitMutation(pm=0.1)

        # Create genetic algorithm engine.
        engine = GAEngine(population=population, selection=selection,
                          crossover=crossover, mutation=mutation)

        @engine.fitness_register
        @engine.minimize
        def fitness(indv):
            x, = indv.solution
            return x + 10*sin(5*x) + 7*cos(4*x)

        engine.run(50)

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(GAEngineTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

