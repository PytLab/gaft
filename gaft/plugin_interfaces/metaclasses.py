#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import inspect
import functools

from ..components.individual import GAIndividual
from ..components.population import GAPopulation
from ..mpiutil import master_only


class AnalysisMeta(type):
    '''
    Metaclass for analysis plugin class
    '''
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
                    attrs[method_name] = lambda self, ng, engine: None
                elif method_name == 'register_step':
                    attrs[method_name] = lambda self, g, population, engine: None
                elif method_name == 'finalize':
                    attrs[method_name] = lambda self, population, engine: None

        # Check if the plugin is only used in master process.
        called_in_master = attrs['master_only'] if 'master_only' in attrs else False

        # Wrap all interfaces.
        if called_in_master:
            for method_name in ['setup', 'register_step', 'finalize']:
                attrs[method_name] = master_only(attrs[method_name])

        # Set logger.
        logger_name = 'gaft.{}'.format(name)
        attrs['logger'] = logging.getLogger(logger_name)

        return type.__new__(cls, name, bases, attrs)


class CrossoverMeta(type):
    '''
    Metaclass for crossover operator class.
    '''
    def __new__(cls, name, bases, attrs):
        if 'cross' not in attrs:
            raise AttributeError('crossover operator class must have cross method')

        if 'pc' in attrs and (attrs['pc'] <= 0.0 or attrs['pc'] > 1.0):
            raise ValueError('Invalid crossover probability')

        cross = attrs['cross']

        # Check parameter of cross method.
        sig = inspect.signature(cross)
        if 'father' not in sig.parameters:
            raise NameError('cross method must have father parameter')
        if 'mother' not in sig.parameters:
            raise NameError('cross method must have mother parameter')

        # Add parameter check to user-defined method.
        @functools.wraps(cross)
        def _wrapped_cross(self, father, mother):
            ''' Wrapper to add parameters type checking.
            '''
            # Check parameter types.
            if not (isinstance(father, GAIndividual) and
                    isinstance(mother, GAIndividual)):
                raise TypeError('father and mother must be GAIndividual object')

            return cross(self, father, mother)

        attrs['cross'] = _wrapped_cross

        return type.__new__(cls, name, bases, attrs)


class MutationMeta(type):
    '''
    Metaclass for mutation operator class.
    '''
    def __new__(cls, name, bases, attrs):
        if 'mutate' not in attrs:
            raise AttributeError('mutation operator class must have mutate method')

        if 'pm' in attrs and (attrs['pm'] <= 0.0 or attrs['pm'] > 1.0):
            raise ValueError('Invalid mutation probability')

        mutate = attrs['mutate']

        # Check parameters of mutate method.
        sig = inspect.signature(mutate)
        if 'individual' not in sig.parameters:
            raise NameError('mutate method must have individual parameter')

        # Add parameter check to user-defined method.
        @functools.wraps(mutate)
        def _wrapped_mutate(self, individual):
            ''' Wrapper to add parameters type checking.
            '''
            # Check parameter types.
            if not isinstance(individual, GAIndividual):
                raise TypeError('individual must be a GAIndividual object')

            return mutate(self, individual)

        attrs['mutate'] = _wrapped_mutate

        return type.__new__(cls, name, bases, attrs)


class SelectionMeta(type):
    '''
    Metaclass for selection operator class.
    '''
    def __new__(cls, name, bases, attrs):
        # Check select method.
        if 'select' not in attrs:
            raise AttributeError('selection operator class must have select method')

        select = attrs['select']

        # Check select arguments.
        sig = inspect.signature(select)
        if 'population' not in sig.parameters:
            raise NameError('select method must have population parameter')
        if 'fitness' not in sig.parameters:
            raise NameError('select method must have fitness parameter')

        # Add parameter check to user-defined method.
        @functools.wraps(select)
        def _wrapped_select(self, population, fitness):
            ''' Wrapper to add parameters type checking.
            '''
            # Check parameter types.
            if not isinstance(population, GAPopulation):
                raise TypeError('father and mother must be GAIndividual object')
            if not callable(fitness):
                raise TypeError('fitness must be a callable object')

            return select(self, population, fitness)

        attrs['select'] = _wrapped_select

        return type.__new__(cls, name, bases, attrs)

