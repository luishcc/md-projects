import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


# R = 6
# ratio = 48
# A = -60
# grid = 1
# sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'
#
# path_to_data = os.getcwd()
# # dir = '/'.join([path_to_data, sim_case, f'grid_{grid}/correlation'])
# dir = '/'.join([path_to_data, sim_case])


# dir = 'thread-2/force_r'
# dir = 'thread/cross'
dir = 'thread3-sat/velocity'
# dir = 'thread/density'
dir_out = '/'.join([dir, 'fig'])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

snap = 500
file = dir + f'/{snap}.dat'
while os.path.isfile(file):
    print(file)
    data = read_dat(file)

    plt.figure(1)

    for i in [1, 6]:
        # print(data[str(i-1)])
        if not np.any(np.isnan(data[str(i-1)])):
            plt.plot(data['dz'][1:], data[str(i-1)][1:],  label=f'r={i-1}')
        else:
            print(i)



    plt.xlabel(r'$\delta z$')
    plt.ylabel(r'$G(r,\delta z)$')
    plt.title(f' Snapshot = {snap}')
    plt.ylim(-0.8, 0.9)
    # plt.xlim(0, 110)
    plt.plot([0, data['dz'][-1]], [0, 0], 'k--')
    plt.legend(loc='lower left')
    plt.savefig(f'{dir_out}/{snap}.png', format='png')
    # plt.show(block=False)
    plt.close(1)
    snap += 6
    file = dir + f'/{snap}.dat'
