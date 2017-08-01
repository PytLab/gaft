#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

from best_fit import best_fit

steps, variants, fits = list(zip(*best_fit))
best_step, best_v, best_f = steps[-1], variants[-1], fits[-1]

fig = plt.figure()

ax = fig.add_subplot(111)
ax.plot(steps, fits)
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness')

# Plot the maximum.
ax.scatter([best_step], [best_f], facecolor='r')
ax.annotate(s='x: [{:.2f}, {:.2f}]\ny:{:.2f}'.format(*best_v, best_f),
                                                     xy=(best_step, best_f),
                                                     xytext=(best_step, best_f-0.1))


plt.show()

