#!/usr/bin/env python
# -*- coding: utf-8 -*-

from best_fit import best_fit

import matplotlib.pyplot as plt

steps, fits = list(zip(*best_fit))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(steps, fits)
ax.set_xlabel('generation')
ax.set_ylabel('fitness')

# Plot the maximum.
x, y = steps[-1], fits[-1]
ax.scatter([x], [y], facecolor='r')
ax.annotate(s='x: {}\ny:{:.2f}'.format(x, y), xy=(x, y), xytext=(x-0.3, y-0.3))

plt.show()

