#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis


class ConsoleOutput(OnTheFlyAnalysis):

    # Analysis interval.
    interval = 1

    # Only analyze in master process?
    master_only = True

    def setup(self, ng, engine):
        generation_info = 'Generation number: {}'.format(ng)
        population_info = 'Population number: {}'.format(engine.population.size)
        self.logger.info('{} {}'.format(generation_info, population_info))

    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        ng_info = 'Generation: {}, '.format(g+1)
        fit_info = 'best fitness: {:.3f}'.format(engine.fitness(best_indv))
        msg = ng_info + fit_info
        self.logger.info(msg)

    def finalize(self, population, engine):
        best_indv = population.best_indv(engine.fitness)
        x = best_indv.variants
        y = engine.fitness(best_indv)
        msg = 'Optimal solution: ({}, {})'.format(x, y)
        self.logger.info(msg)

