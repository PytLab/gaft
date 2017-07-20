#!/usr/bin/env python
# -*- coding: utf-8 -*-

class OnTheFlyAnalysis(object):
    '''
    Class for providing an interface to easily extend and customize the behavior
    of the on-the-fly analysis functionality of gapy.
    '''

    def __init__(self, interval):
        '''
        The constructor of the base-class.

        :param interval: analysis interval.
        :type interval: int
        '''
        self.interval = interval

    def setup(self, population, engine):
        '''
        Function called right before the start of genetic algorithm main iteration
        to allow for custom setup of the analysis object.

        :param population: The up to date population of the iteration.
        :type population: GAPopulation

        :param engine: The current GAEngine where the analysis is running.
        :type engine: GAEngine
        '''
        raise NotImplementedError

    def register_step(self, ng, population, engine):
        '''
        Function called in each iteration step.

        :param ng: Current generation number.
        :type ng: int

        :param population: The up to date population of the iteration.
        :type population: GAPopulation

        :param engine: The current GAEngine where the analysis is running.
        :type engine: GAEngine
        '''
        raise NotImplementedError

    def finalize(self):
        '''
        Called after the iteration to allow for custom finalization and
        post-processing of the collected data.
        '''
        raise NotImplementedError

