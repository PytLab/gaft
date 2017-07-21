#!/usr/bin/env python
# -*- coding: utf-8 -*-

class OnTheFlyAnalysis(metaclass=AnalysisMeta):
    '''
    Class for providing an interface to easily extend and customize the behavior
    of the on-the-fly analysis functionality of gapy.
    '''

    # Analysis interval.
    interval = 1

    def __init__(self, *kwargs):
        '''
        The constructor of the base-class.
        '''
        pass

    def setup(self, population, engine, **kwargs):
        '''
        Function called right before the start of genetic algorithm main iteration
        to allow for custom setup of the analysis object.

        :param population: The up to date population of the iteration.
        :type population: GAPopulation

        :param engine: The current GAEngine where the analysis is running.
        :type engine: GAEngine

        **You can also add more custom parameters to this method.**
        '''
        raise NotImplementedError

    def register_step(self, ng, population, engine, **kwargs):
        '''
        Function called in each iteration step.

        :param ng: Current generation number.
        :type ng: int

        :param population: The up to date population of the iteration.
        :type population: GAPopulation

        :param engine: The current GAEngine where the analysis is running.
        :type engine: GAEngine

        **You can also add more custom parameters to this method.**
        '''
        raise NotImplementedError

    def finalize(self):
        '''
        Called after the iteration to allow for custom finalization and
        post-processing of the collected data.
        '''
        raise NotImplementedError


class AnalysisMeta(type):
    '''
    Metaclass for analysis plugin class
    '''
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, attrs):
        # Check interval type.
        if 'interval' in attrs:
            interval = attrs['interval']
            if type(interval) is not int or interval <= 0:
                raise TypeError('analysis interval must be a positive integer')

        for method_name in ['setup', 'register_step', 'finalize']:
            method = attrs.get(method_name, None)
            if not callable(method):
                msg = "'setup', 'register_step' and 'finalize' must be defiend as method"
                raise AttributeError(msg)

        return cls

