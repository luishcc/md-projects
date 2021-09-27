import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


R = 6
ratio = 48
A = -60
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

    for i in range(1, len(data)):
        if not np.any(np.isnan(data[str(i-1)])):
            plt.plot(data['freq'], data[str(i-1)],
                     label=f'R={i-1}')



    plt.xlabel(r'Frequency')
    plt.ylabel(r'Fourier')
    plt.title(f'R = {R}, Ratio = {ratio}, Snapshot = {snap}')
    plt.grid(True)
    plt.ylim(-0.05, 35)
    plt.xlim(-0.01, 0.15)
    plt.plot([0, data['freq'][-1]], [0, 0], 'k--')
    plt.legend(loc='right')
    plt.savefig(f'{dir_out}/{snap}.png', format='png')
    plt.close(1)
    snap += 1
    file = dir + f'/{snap}.dat'
