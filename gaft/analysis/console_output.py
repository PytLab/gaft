#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis
from ..mpiutil import master_only

class ConsoleOutputAnalysis(OnTheFlyAnalysis):

    interval = 1

    @master_only
    def setup(self, ng, engine):
        generation_info = 'Generation number: {}'.format(ng)
        population_info = 'Population number: {}'.format(engine.population.size)
        engine.logger.info('{} {}'.format(generation_info, population_info))

    @master_only
    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        ng_info = 'Generation: {}, '.format(g)
        fit_info = 'best fitness: {:.3f}'.format(engine.fitness(best_indv))
        msg = ng_info + fit_info
        engine.logger.info(msg)

    @master_only
    def finalize(self, population, engine):
        best_indv = population.best_indv(engine.fitness)
        x = best_indv.variants
        y = engine.fitness(best_indv)
        msg = 'Optimal solution: ({}, {})'.format(x, y)
        engine.logger.info(msg)

