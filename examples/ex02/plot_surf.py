#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import numpy as np
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt

from best_fit import best_fit

for i, (x, y), z in best_fit:
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter([x], [y], [z], zorder=99, c='r', s=100)

    x, y = np.mgrid[-2:2:100j, -2:2:100j]
    z = y*np.sin(2*np.pi*x) + x*np.cos(2*np.pi*y)
    ax.plot_surface(x, y, z, rstride=2, cstride=1, cmap=plt.cm.bone_r)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if not os.path.exists('./surfaces'):
        os.mkdir('./surfaces')
    fig.savefig('./surfaces/{}.png'.format(i))
    print('save ./surfaces/{}.png'.format(i))
    plt.close(fig)

