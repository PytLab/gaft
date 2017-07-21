#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Find the global maximum for function: f(x) = x + 10sin(5x) + 7cos(4x)
'''

from math import sin, cos

from gapy import GAEngine
from gapy.components import GAIndividual
from gapy.components import GAPopulation
from gapy.operators import RouletteWheelSelection
from gapy.operators import UniformCrossover
from gapy.operators import FlipBitMutation
from gapy.analysis import ConsoleOutputAnalysis

# Define population.
indv_template = GAIndividual(ranges=[(0, 10)], encoding='binary', eps=0.001)
population = GAPopulation(indv_template=indv_template, size=50)

# Create genetic operators.
selection = RouletteWheelSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)

# Create genetic algorithm engine.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation, analysis=[ConsoleOutputAnalysis])

# Define fitness function.
@engine.fitness_register
def fitness(indv):
    x, = indv.variants
    return x + 10*sin(5*x) + 7*cos(4*x)


if '__main__' == __name__:
    engine.run(ng=100)

