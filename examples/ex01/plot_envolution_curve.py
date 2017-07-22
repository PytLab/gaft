#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sin, cos
import numpy as np
import matplotlib.pyplot as plt
from best_fit import best_fit

steps, variants, fits = list(zip(*best_fit))
best_step, best_v, best_f = steps[-1], variants[-1][0], fits[-1]

fig = plt.figure()

ax = fig.add_subplot(211)
f = lambda x: x + 10*sin(5*x) + 7*cos(4*x)
x = np.linspace(0, 10, 1000)
y = [f(i) for i in x]
ax.plot(x, y)
ax.scatter([best_v], [best_f], facecolor='r')
ax.set_xlabel('x')
ax.set_ylabel('y')

ax = fig.add_subplot(212)
ax.plot(steps, fits)
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')

# Plot the maximum.
ax.scatter([best_step], [best_f], facecolor='r')
ax.annotate(s='x: {:.2f}\ny:{:.2f}'.format(best_v, best_f),
                                           xy=(best_step, best_f),
                                           xytext=(best_step-0.3, best_f-0.3))


plt.show()

