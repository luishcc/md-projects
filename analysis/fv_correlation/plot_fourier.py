import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


# dir = 'thread/force_r/fourier'
# dir = 'thread/cross'
dir = 'thread/velocity_z/fourier'
# dir = 'thread/density'

dir_out = '/'.join([dir, 'fig'])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

snap = 0
file = dir + f'/{snap}.dat'
while os.path.isfile(file):
    print(file)
    data = read_dat(file)

    plt.figure(1)

    for i in range(1, 5): #len(data)
        if not np.any(np.isnan(data[str(i-1)])):
            plt.plot(data['freq'][1:], data[str(i-1)][1:],
                     label=f'r={i-1}', marker='.')



    plt.xlabel(r'Frequency')
    plt.ylabel(r'Fourier of $G(r,\delta z)$')
    plt.title(f'Snapshot = {snap}')
    plt.grid(True)
    plt.ylim(-1.05, 3)
    # plt.xlim(-0.0, 0.10)
    plt.plot([0, data['freq'][-1]], [0, 0], 'k--')
    plt.legend(loc='right')
    plt.savefig(f'{dir_out}/{snap}.png', format='png')
    plt.close(1)
    snap += 6
    file = dir + f'/{snap}.dat'
