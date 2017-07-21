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

def suite():
    test_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(IndividualTest),
        unittest.TestLoader().loadTestsFromTestCase(PopulationTest),
        unittest.TestLoader().loadTestsFromTestCase(RouletteWheelSelectionTest),
        unittest.TestLoader().loadTestsFromTestCase(UniformCrossoverTest),
        unittest.TestLoader().loadTestsFromTestCase(FlipBitMutationTest),
    ])

    return test_suite

if '__main__' == __name__:
    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.errors or result.failures:
        raise ValueError('Get erros and failures')

