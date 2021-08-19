import numpy as np
import sys
import os

from mdpkg.rwfile import DumpReader
from mdpkg.grid import Grid

from math import floor, ceil

from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq

import matplotlib.pyplot as plt


# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "sans-serif",
#     "font.size": 14,
#     "font.sans-serif": ["Helvetica"]})


trj = DumpReader('thread.lammpstrj')

trj.read_sequential()

rrange = 10
size =1

fourier_r = ceil((rrange/2)*1.25)
iter = 0

skip = 4

while True:

    print(iter)

    grd = Grid(trj.snap, size=size)
    num = floor(grd.num_z/2)
    dz = np.linspace(0, grd.length_z/2, num)

    plt.figure(1)

    for r in range(rrange):
        a = grd.compute_density_correlation(r)
        plt.plot(dz, a, label=f'R={r}')
        if r == fourier_r:
            f = rfft(a) / len(a)
            freq = rfftfreq(len(a))

            plt.figure(2)
            plt.title(f'Snapshot {iter}')
            plt.plot(freq[:], f.real[:], 'k-', marker='o')
            # plt.ylim(-0.6,3)
            plt.plot([0, 0.2], [0, 0], 'b--')
            plt.xlim(0,0.2)
            plt.savefig(f'gif2/{iter}.png', format='png')
            plt.close(2)

        if float('Nan') in a:
            continue

    plt.title(f'Snapshot {iter}')
    plt.xlabel(r'$\delta z$')
    plt.ylabel(r'$G(r,\delta z)$')
    plt.ylim(-0.05, 1.1)
    plt.plot([0, grd.length_z/2], [0, 0], 'k--')
    plt.legend(loc='right')
    plt.savefig(f'gif/{iter}.png', format='png')
    plt.close(1)

    try:
        rd.skip_next(skip)
        rd.read_next()
        iter += (skip + 1)
    except ValueError:
        break
