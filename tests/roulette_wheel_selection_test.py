#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for built-in Roulette Wheel selection
'''

import unittest

from gapy.components.population import GAPopulation
from gapy.components.individual import GAIndividual
from gapy.operators.builtin.selection.roulette_wheel_selection import RouletteWheelSelection

class RouletteWheelSelectionTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff
        def fitness(indv):
            x, = indv.variants
            return x**3 - 60*x**2 + 900*x + 100
        self.fitness = fitness

    def test_selection(self):
        indv = GAIndividual(ranges=[(0, 30)])
        p = GAPopulation(indv, fitness=self.fitness)
        p.init()

        selection = RouletteWheelSelection()
        father, mother = selection.select(p)

        self.assertTrue(isinstance(father, GAIndividual))
        self.assertTrue(isinstance(mother, GAIndividual))
        self.assertNotEqual(father.chromsome, mother.chromsome)

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(RouletteWheelSelectionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

