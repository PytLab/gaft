#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import uniform
from copy import deepcopy


class SolutionRanges(object):
    ''' Descriptor for solution ranges.
    '''
    def __init__(self):
        self.__ranges = []

    def __get__(self, obj, owner):
        return self.__ranges

    def __set__(self, obj, ranges):
        # Check.
        if type(ranges) not in [tuple, list]:
            raise TypeError('solution ranges must be a list of range tuples')
        for rng in ranges:
            if type(rng) not in [tuple, list]:
                raise TypeError('range({}) is not a tuple containing two numbers'.format(rng))
            if len(rng) != 2:
                raise ValueError('length of range({}) not equal to 2')
            a, b = rng
            if a >= b:
                raise ValueError('Wrong range value {}'.format(rng))
        # Assignment.
        self.__ranges = ranges


class DecretePrecision(object):
    ''' Descriptor for individual decrete precisions.
    '''
    def __init__(self):
        self.__precisions = []

    def __get__(self, obj, owner):
        return self.__precisions

    def __set__(self, obj, precisions):
        if type(precisions) in [int, float]:
            precisions = [precisions]*len(obj.ranges)
        # Check.
        if type(precisions) not in [tuple, list]:
            raise TypeError('precisions must be a list of numbers')
        if len(precisions) != len(obj.ranges):
            raise ValueError('Lengths of eps and ranges should be the same')
        for (a, b), eps in zip(obj.ranges, precisions):
            if eps > (b - a):
                msg = 'Invalid precision {} in range ({}, {})'.format(eps, a, b)
                raise ValueError(msg)
        self.__precisions = precisions


class IndividualBase(object):
    ''' Base class for individuals.
    '''
    # Solution ranges.
    ranges = SolutionRanges()

    # Original decrete precisions (provided by users).
    eps = DecretePrecision()
    
    # Actual decrete precisions used in GA.
    precisions = DecretePrecision()

    def __init__(self, ranges, eps):
        self.ranges = ranges
        self.eps = eps
        self.precisions = eps

        self.solution, self.chromsome = [], []

    def init(self, chromsome=None, solution=None):
        '''
        Initialize the individual by providing chromsome or solution.

        If both chromsome and solution are provided, only the chromsome would
        be used. If neither is provided, individual would be initialized randomly.

        :param chromsome: chromesome sequence for the individual
        :type chromsome: list of float/int.

        :param solution: the variable vector of the target function.
        :type solution: list of float.
        '''
        if not any([chromsome, solution]):
            self.solution = self._rand_solution()
            self.chromsome = self.encode()
        elif chromsome:
            self.chromsome = chromsome
            self.solution = self.decode()
        else:
            self.solution = solution
            self.chromsome = self.encode()

        return self

    def clone(self):
        '''
        Clone a new individual from current one.
        '''
        indv = self.__class__(deepcopy(self.ranges), eps=deepcopy(self.eps))
        indv.init(chromsome=deepcopy(self.chromsome))
        return indv


    def encode(self):
        ''' *NEED IMPLIMENTATION*
        Convert solution to chromsome sequence.

        :return chromsome: The chromsome sequence, float list.
        '''
        raise NotImplementedError

    def decode(self):
        ''' *NEED IMPLIMENTATION*
        Convert chromsome sequence to solution.

        :return solution: The solution vector, float list.
        '''
        raise NotImplementedError

    def _rand_solution(self):
        ''' Initialize individual solution randomly.
        '''
        solution = []
        for eps, (a, b) in zip(self.precisions, self.ranges):
            n_intervals = (b - a)//eps
            n = int(uniform(0, n_intervals + 1))
            solution.append(a + n*eps)
        return solution


