#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy
from random import random

from ...plugin_interfaces.operators.crossover import GACrossover


class UniformCrossover(GACrossover):
    def __init__(self, pc, pe=0.5):
        '''
        Crossover operator with uniform crossover algorithm,
        see https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)

        :param pc: Crossover probability.
        :param pe: Gene exchange probability.
        '''
        super(self.__class__, self).__init__(pc=pc)
        self.pe = pe

    def cross(self, father, mother):
        '''
        Cross chromsomes of parent using uniform crossover method.
        '''
        do_cross = True if random() <= self.pc else False

        if not do_cross:
            return father, mother

        # Chromsomes for two children.
        chrom1 = father.chromsome.copy()
        chrom2 = mother.chromsome.copy()

        for i, (g1, g2) in enumerate(zip(chrom1, chrom2)):
            do_exchange = True if random() < self.pe else False
            if do_exchange:
                chrom1[i], chrom2[i] = g2, g1

        child1, child2 = father.clone(), father.clone()
        child1.init(chromsome=chrom1)
        child2.init(chromsome=chrom2)

        return child1, child2

