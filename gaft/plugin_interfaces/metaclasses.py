#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from ..mpiutil import master_only


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
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, attrs):
        if 'cross' not in attrs:
            raise AttributeError('crossover operator class must have cross method')

        if 'pc' in attrs and (attrs['pc'] <= 0.0 or attrs['pc'] > 1.0):
            raise ValueError('Invalid crossover probability')

        return type.__new__(cls, name, bases, attrs)


class MutationMeta(type):
    '''
    Metaclass for mutation operator class.
    '''
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, attrs):
        if 'mutate' not in attrs:
            raise AttributeError('mutation operator class must have mutate method')

        if 'pm' in attrs and (attrs['pm'] <= 0.0 or attrs['pm'] > 1.0):
            raise ValueError('Invalid mutation probability')

        return type.__new__(cls, name, bases, attrs)


class SelectionMeta(type):
    '''
    Metaclass for selection operator class.
    '''
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        return {}

    def __new__(cls, name, bases, attrs):
        if 'select' not in attrs:
            raise AttributeError('selection operator class must have select method')

        return type.__new__(cls, name, bases, attrs)

