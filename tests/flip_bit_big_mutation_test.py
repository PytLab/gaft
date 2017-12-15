#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for built-in Flip Bit mutation operator with big mutation rate.
'''

import unittest
from math import sin, cos

from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import Population
from gaft.operators import RouletteWheelSelection
from gaft.operators import UniformCrossover
from gaft.operators.mutation.flip_bit_mutation import FlipBitBigMutation

class FlipBitBigMutationTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff

    def test_mutate(self):
        ''' Make sure the individual can be mutated correctly.
        '''
        indv_template = BinaryIndividual(ranges=[(0, 10)], eps=0.001)
        population = Population(indv_template=indv_template, size=50).init()

        # Create genetic operators.
        selection = RouletteWheelSelection()
        crossover = UniformCrossover(pc=0.8, pe=0.5)
        mutation = FlipBitBigMutation(pm=0.03, pbm=0.2, alpha=0.6)

        # Create genetic algorithm engine.
        engine = GAEngine(population=population, selection=selection,
                          crossover=crossover, mutation=mutation)

        @engine.fitness_register
        def fitness(indv):
            x, = indv.solution
            return x + 10*sin(5*x) + 7*cos(4*x)

        mutation.mutate(indv_template, engine)

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(FlipBitBigMutationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

