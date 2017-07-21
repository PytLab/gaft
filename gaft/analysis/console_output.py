#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..plugin_interfaces.analysis import OnTheFlyAnalysis

class ConsoleOutputAnalysis(OnTheFlyAnalysis):

    interval = 1

    def register_step(self, ng, population, engine):
        best_indv = population.best_indv(engine.fitness)
        msg = 'Generation: {}, best fitness: {:.3f}'.format(ng, engine.fitness(best_indv))
        engine.logger.info(msg)

