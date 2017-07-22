#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis

class FitnessStoreAnalysis(OnTheFlyAnalysis):

    interval = 1

    def setup(self, population, engine):
        # Generation numbers.
        self.ngs = []

        # Best fitness in each generation.
        self.fitness_values = []

        # Best variants.
        self.variants = []

    def register_step(self, ng, population, engine):
        # Collect data.
        best_indv = population.best_indv(engine.fitness)
        best_fit = engine.fitness(best_indv)

        self.ngs.append(ng)
        self.variants.append(best_indv.variants)
        self.fitness_values.append(best_fit)

    def finalize(self, population, engine):
        with open('best_fit.py', 'w', encoding='utf-8') as f:
            f.write('best_fit = [\n')
            for ng, x, y in zip(self.ngs, self.variants, self.fitness_values):
                f.write('    ({}, {}, {}),\n'.format(ng, x, y))
            f.write(']\n\n')

        engine.logger.info('Best fitness values are written to best_fit.py')

