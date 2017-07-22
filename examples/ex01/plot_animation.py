#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sin, cos
import numpy as np
import matplotlib.pyplot as plt
from best_fit import best_fit


for i, (x,), y in best_fit:
    fig = plt.figure(figsize=(12, 8))

    ax = fig.add_subplot(111)
    f = lambda x: x + 10*sin(5*x) + 7*cos(4*x)
    xs = np.linspace(0, 10, 1000)
    ys = [f(i) for i in xs]
    ax.plot(xs, ys)
    ax.scatter([x], [y], facecolor='r', s=100)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    fig.savefig('{}.png'.format(i))
    print('save {}.png'.format(i))
    plt.close(fig)

