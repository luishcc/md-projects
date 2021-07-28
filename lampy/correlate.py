import numpy as np


def correlate(grid, r, dz, rho):

    num_phi = grid.get_numphi(r)

    sumsq = 0
    corr = 0
    for z in range(grid.num_z - dz):
        for phi in range(num_phi):
            try:
                sumsq += grid.cell[(r, phi, z)].get_density()**2
                corr += grid.cell[(r, phi, z)].get_density() \
                      * grid.cell[(r, phi, z+dz)].get_density()
            except KeyError:
                continue

    for i in range(z+1, grid.num_z):
        for phi in range(num_phi):
            try:
                sumsq += grid.cell[(r, phi, i)].get_density()**2
            except KeyError:
                continue


    nn = (grid.num_z-dz) * num_phi
    nn2 = (grid.num_z) * num_phi

    try:
        corr2 = corr/ nn  #* rho**2
        corr /= (sumsq / nn2) * nn

    except ZeroDivisionError:
        return float('NaN')



    return corr - 1 , corr2


import sys
import os
sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy')
from grid import Grid
from readLammps import DumpReader
from math import floor


data = DumpReader('dump.corr')
grd = Grid(data, size = float(sys.argv[1]))


num = floor(grd.num_z/2)
# num = grd.num_z

def run(r):
    cor = np.zeros(num)
    rho = np.zeros(num)

    for dz in range(num):
        cor[dz], rho[dz] = correlate(grd, r, dz, 7)
    return cor, rho

res = []
rho = []
rrange = 5
for r in range(rrange):
    a, b = run(r)
    res.append(a)
    rho.append(b)

import matplotlib.pyplot as plt

plt.figure(1)
for r in range(rrange):
    if float('Nan') in res[r]:
        continue
    plt.plot(np.linspace(0,num-1, num), res[r], label=f'R={r}')
plt.legend()

plt.figure(2)
for r in range(rrange):
    if float('Nan') in rho[r]:
        continue
    plt.plot(np.linspace(0,num-1, num), rho[r], label=f'R={r}')
plt.legend()

plt.show()

# idr = []
# idz = []
# d = []
# for key, cell in grd.cell.items():
#     idr.append(cell.id[0])
#     idz.append(cell.id[2])
#     d.append(cell.get_density()/cell.nangle)
#
# from scipy.sparse import coo_matrix
# coo = coo_matrix((d, (idr, idz)))
#
# coo = coo.todense().transpose()
#
#
# fig, ax = plt.subplots(1,1)
# im = ax.imshow(coo, extent=[0, 1, 0, 1], aspect=10)
# fig.colorbar(im)
# ax.set_xlabel('Radius')
# ax.set_ylabel('Length')
# ax.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
# ax.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks

# plt.show()
