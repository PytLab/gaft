#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis
from ..mpiutil import master_only

class FitnessStoreAnalysis(OnTheFlyAnalysis):

    interval = 1

    @master_only
    def setup(self, ng, engine):
        # Generation numbers.
        self.ngs = []

        # Best fitness in each generation.
        self.fitness_values = []

        # Best variants.
        self.variants = []

    @master_only
    def register_step(self, g, population, engine):
        # Collect data.
        best_indv = population.best_indv(engine.fitness)
        best_fit = engine.fitness(best_indv)

        self.ngs.append(g)
        self.variants.append(best_indv.variants)
        self.fitness_values.append(best_fit)

    @master_only
    def finalize(self, population, engine):
        with open('best_fit.py', 'w', encoding='utf-8') as f:
            f.write('best_fit = [\n')
            for ng, x, y in zip(self.ngs, self.variants, self.fitness_values):
                f.write('    ({}, {}, {}),\n'.format(ng, x, y))
            f.write(']\n\n')

        engine.logger.info('Best fitness values are written to best_fit.py')

