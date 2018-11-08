#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Test case for built-in Tournament Selection operator.
'''

import unittest

from gaft.components import Population, BinaryIndividual
from gaft.operators import TournamentSelection

class TournamentSelectionTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff
        def fitness(indv):
            x, = indv.solution
            return x**3 - 60*x**2 + 900*x + 100
        self.fitness = fitness

    def test_selection(self):
        indv = BinaryIndividual(ranges=[(0, 30)])
        p = Population(indv)
        p.init()

        selection = TournamentSelection()
        father, mother = selection.select(p, fitness=self.fitness)

        self.assertTrue(isinstance(father, BinaryIndividual))
        self.assertTrue(isinstance(mother, BinaryIndividual))

if '__main__' == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(TournamentSelectionTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

