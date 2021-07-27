import numpy as np


def correlate(grid, r, dz):

    num_t = gird.get_numphi(r)

    sum = 0
    sumsq = 0

    corr = 0

    for z in range(grid.num_z - dz):
        for t in range(num_t):
            try:
                corr += grid.cell[(r, t, z)].get_density() \
                      * grid.cell[(r, t, z+1)].get_density()
                sum += grid.cell[(r, t, z)].get_density()
                sumsq += grid.cell[(r, t, z)].get_density()**2
            except:
                continue

    nn = (grid.num_z * num_t)
    var = (sumsq - (sum**2/nn))
    corr = corr / var

    return corr


import sys
import os
sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy')
from grid import Grid
