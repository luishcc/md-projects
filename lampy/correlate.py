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
        # corr = corr/ nn  #* rho**2
        corr /= (sumsq / nn2) * nn

    except ZeroDivisionError:
        return float('NaN')



    return corr  #, corr2


import sys
import os
sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy')
from grid import Grid
from readLammps import DumpReader
from math import floor


data = DumpReader('dump.corr2')
grd = Grid(data, size = float(sys.argv[1]))


num = floor(grd.num_z/2)
# num = grd.num_z

def run(r):
    cor = np.zeros(num)
    rho = np.zeros(num)

    for dz in range(num):
        cor[dz] = correlate(grd, r, dz, 7)
    return cor

res = []
# rho = []
rrange = int(sys.argv[2])
for r in range(rrange):
    a = run(r)
    res.append(a)
    # rho.append(b)

import matplotlib.pyplot as plt

# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "sans-serif",
#     "font.size": 14,
#     "font.sans-serif": ["Helvetica"]})

plt.figure(1)
print(grd.length_z)
for r in range(rrange):
    if float('Nan') in res[r]:
        continue
    plt.plot(np.linspace(0, grd.length_z/2, num), res[r], label=f'R={r}')
plt.xlabel(r'$\delta z$')
plt.ylabel(r'$G(r,\delta z)$')
plt.legend(loc='right')


from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq

f = fftshift(fft(res[5]))
freq = fftshift(fftfreq(len(res[5])))

f = rfft(res[5]) / len(res[5])
freq = rfftfreq(len(res[5]))

plt.figure(2)
plt.plot(freq[:], f.real[:], 'k-', marker='o')
# plt.plot([min(freq[1:20]), max(freq[1:20])], [0,0], 'r-.')
# plt.ylim(-0.6,3)
plt.xlim(0,0.2)

# plt.plot(freq, f.imag, 'b-')

# spec = np.abs(f)**2

# plt.subplot(133)
# plt.plot(freq, spec/max(spec), 'b-')

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
# fig.set_dpi(460)


plt.show()
