import numpy as np


def correlate(grid, r, dz, rho):

    num_phi = grid.get_numphi(r)

    sum = 0
    sumsq = 0

    corr = 0

    for z in range(grid.num_z - dz):
        for phi in range(num_phi):
            try:
                # sum += grid.cell[(r, phi, z)].get_density()
                sumsq += grid.cell[(r, phi, z)].get_density()**2
                corr += grid.cell[(r, phi, z)].get_density() \
                      * grid.cell[(r, phi, z+dz)].get_density()
                # print(phi, z, corr)

            except KeyError:
                continue

    nn = (grid.num_z * num_phi)

    # corr /= nn * rho**2

    try:
        corr /= sumsq
    except ZeroDivisionError:
        return float('NaN')

    # var = (sumsq - (sum**2/nn))
    # corr = corr / var

    return corr - 1


import sys
import os
sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy')
from grid import Grid
from readLammps import DumpReader
from math import floor


data = DumpReader('dump.corr')
grd = Grid(data, size = float(sys.argv[1]))


num = floor(grd.num_z/2)
def run(r):
    cor = np.zeros(num)
    for dz in range(num):
        cor[dz] = correlate(grd, r, dz, 7)
    return cor

res = []
rrange = 7
for r in range(rrange):
    res.append(run(r))

import matplotlib.pyplot as plt

plt.figure(1)
for r in range(rrange):
    plt.plot(np.linspace(0,num-1, num), res[r], label=f'R={r}')
plt.legend()
plt.show()
