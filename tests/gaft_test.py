#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Module for all test in ga.py
'''

import unittest

from individual_test import IndividualTest
from population_test import PopulationTest
from roulette_wheel_selection_test import RouletteWheelSelectionTest
from uniform_crossover_test import UniformCrossoverTest
from flip_bit_mutation_test import FlipBitMutationTest
from mpiutil_test import MPIUtilTest
from engine_test import GAEngineTest
from tournament_selection_test import TournamentSelectionTest
from linear_ranking_selection_test import LinearRankingSelectionTest
from exponential_ranking_selection_test import ExponentialRankingSelectionTest

def suite():
    test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(IndividualTest),
        unittest.TestLoader().loadTestsFromTestCase(PopulationTest),
        unittest.TestLoader().loadTestsFromTestCase(RouletteWheelSelectionTest),
        unittest.TestLoader().loadTestsFromTestCase(UniformCrossoverTest),
        unittest.TestLoader().loadTestsFromTestCase(FlipBitMutationTest),
        unittest.TestLoader().loadTestsFromTestCase(MPIUtilTest),
        unittest.TestLoader().loadTestsFromTestCase(GAEngineTest),
        unittest.TestLoader().loadTestsFromTestCase(TournamentSelectionTest),
        unittest.TestLoader().loadTestsFromTestCase(LinearRankingSelectionTest),
        unittest.TestLoader().loadTestsFromTestCase(ExponentialRankingSelectionTest),
    ])

    return test_suite

if '__main__' == __name__:
    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.errors or result.failures:
        raise ValueError('Get erros and failures')

