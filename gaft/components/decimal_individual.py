#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Definition of individual class with decimal encoding.
'''

from .individual import IndividualBase


class DecimalIndividual(IndividualBase):
    ''' Individual with decimal encoding.
    '''
    def __init__(self, ranges, eps=0.001):
        super(self.__class__, self).__init__(ranges, eps)
        # Initialize it randomly.
        self.init()

    def encode(self):
        return self.solution

    def decode(self):
        return self.solution

