#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
            if method is not None and not callable(method):
                msg = "{} must be a callable object".format(method)
                raise AttributeError(msg)
            # Set default interface methods.
            elif method is None:
                if method_name == 'setup':
                    attrs[method_name] = lambda self, population, engine: None
                elif method_name == 'register_step':
                    attrs[method_name] = lambda self, ng, population, engine: None
                elif method_name == 'finalize':
                    attrs[method_name] = lambda self, population, engine: None

        return type.__new__(cls, name, bases, attrs)


class OnTheFlyAnalysis(metaclass=AnalysisMeta):
    '''
    Class for providing an interface to easily extend and customize the behavior
    of the on-the-fly analysis functionality of gapy.
    '''

    # Analysis interval.
    interval = 1

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

    def finalize(self, population, engine):
        '''
        Called after the iteration to allow for custom finalization and
        post-processing of the collected data.

        :param population: The up to date population of the iteration.
        :type population: GAPopulation

        :param engine: The current GAEngine where the analysis is running.
        :type engine: GAEngine
        '''
        raise NotImplementedError

