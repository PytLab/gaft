#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Find the global maximum for function: f(x) = x + 10sin(5x) + 7cos(4x)
'''

from math import sin, cos

from gapy.components.individual import GAIndividual
from gapy.components.population import GAPopulation
from gapy.operators.builtin.selection.roulette_wheel_selection import RouletteWheelSelection
from gapy.operators.builtin.crossover.uniform_crossover import UniformCrossover
from gapy.operators.builtin.mutation.flip_bit_mutation import FlipBitMutation
from gapy.engine import GAEngine

# Define fitness function.
def fitness(indv):
    x, = indv.variants
    return x + 10*sin(5*x) + 7*cos(4*x)

# Define population.
indv_template = GAIndividual(ranges=[(0, 10)], encoding='binary', eps=0.01)
population = GAPopulation(indv_template=indv_template, fitness=fitness, size=50)

# Create genetic operators.
selection = RouletteWheelSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.1)

# Create genetic algorithm engine.
engine = GAEngine(population=population, fitness=fitness, selection=selection,
                  crossover=crossover, mutation=mutation)

engine.run(ng=100)

