import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


R = 8
ratio = 48
A = -50
grid = 1
sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'

path_to_data = os.getcwd()
# dir = '/'.join([path_to_data, sim_case, f'grid_{grid}/fourier'])
dir = '/'.join([path_to_data, sim_case, '/fourier'])

dir_out = '/'.join([dir, 'fig'])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

snap = 0
file = dir + f'/{snap}.dat'
while os.path.isfile(file):
    print(file)
    data = read_dat(file)

    plt.figure(1)

    for i in range(5, 9): #len(data)
        if not np.any(np.isnan(data[str(i-1)])):
            plt.plot(data['freq'][1:], data[str(i-1)][1:],
                     label=f'r={i-1}')



    plt.xlabel(r'Frequency')
    plt.ylabel(r'Fourier of $G(r,\delta z)$')
    plt.title(f'$R_0$ = {R}, Ratio = {ratio}, Snapshot = {snap}')
    plt.grid(True)
    plt.ylim(-0.05, 20)
    plt.xlim(-0.0, 0.10)
    plt.plot([0, data['freq'][-1]], [0, 0], 'k--')
    plt.legend(loc='right')
    plt.savefig(f'{dir_out}/{snap}.png', format='png')
    plt.close(1)
    snap += 1
    file = dir + f'/{snap}.dat'
