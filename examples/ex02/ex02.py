#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Find the global maximum for binary function: f(x) = y*sim(2*pi*x) + x*cos(2*pi*y)
'''

from math import sin, cos, pi

from gaft import GAEngine
from gaft.components import GAIndividual
from gaft.components import GAPopulation
from gaft.operators import RouletteWheelSelection, TournamentSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation

# Built-in best fitness analysis.
from gaft.analysis.fitness_store import FitnessStore
from gaft.analysis.console_output import ConsoleOutput

# Define population.
indv_template = GAIndividual(ranges=[(-2, 2), (-2, 2)],
                             encoding='binary',
                             eps=0.001)
population = GAPopulation(indv_template=indv_template, size=50).init()

# Create genetic operators.
#selection = RouletteWheelSelection()
selection = TournamentSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)

# Create genetic algorithm engine.
# Here we pass all built-in analysis to engine constructor.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation,
                  analysis=[ConsoleOutput, FitnessStore])

# Define fitness function.
@engine.fitness_register
def fitness(indv):
    x, y = indv.variants
    return y*sin(2*pi*x) + x*cos(2*pi*y)

if '__main__' == __name__:
    engine.run(ng=100)

