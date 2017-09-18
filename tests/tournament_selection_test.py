#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for built-in Tournament Selection operator.
'''

import unittest

from gaft.components.population import GAPopulation
from gaft.components.individual import GAIndividual
from gaft.operators import TournamentSelection

class TournamentSelectionTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff
        def fitness(indv):
            x, = indv.variants
            return x**3 - 60*x**2 + 900*x + 100
        self.fitness = fitness

    def test_selection(self):
        indv = GAIndividual(ranges=[(0, 30)])
        p = GAPopulation(indv)
        p.init()

        selection = TournamentSelection()
        father, mother = selection.select(p, fitness=self.fitness)

        self.assertTrue(isinstance(father, GAIndividual))
        self.assertTrue(isinstance(mother, GAIndividual))
        self.assertNotEqual(father.chromsome, mother.chromsome)

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(TournamentSelectionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

