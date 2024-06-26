import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


R = 6
R2 = 5
ratio = 48
A = -60
grid = 1

sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'

path_to_data = os.getcwd()
# dir = '/'.join([path_to_data, sim_case, f'grid_{grid}/fourier'])
dir = '/'.join([path_to_data, sim_case, 'fourier'])


def dict_to_np(dict):
    col = len(dict)
    row = len(dict['freq'])
    data = np.zeros((row, col))
    data[:, 0] = dict['freq']
    for i in range(1, col):
        data[:, i] = dict[str(i-1)]
    return np.nan_to_num(data)

def color(r):
    if (r+1)/R2 < 0.5:
        return 'blue'
    elif 1 > (r+1)/R2 > 0.5:
        return 'red'
    else:
        return 'black'

from_freq = 8
snap = 0
file = dir + f'/{snap}.dat'
plt.figure(1)
while os.path.isfile(file):
    print(file)
    data = read_dat(file)
    data = dict_to_np(data)

    max = np.unravel_index(data[from_freq:, 1:].argmax(),data[2:, 1:].shape)

    # for i in range(1, len(data)):
    # print(max)
    print(data[max[0]+from_freq , 0])
    plt.scatter(snap, 2*np.pi*R2*data[max[0]+from_freq , 0],
                        edgecolors=color(100), facecolors=color(100))
    # print(color(max[1]))

    snap += 1
    file = dir + f'/{snap}.dat'


plt.xlabel(r'Time')
plt.ylabel(r'reduced wavenumber')
plt.title(f'R = {R}, Ratio = {ratio}, A = {A}')
plt.grid(True)
plt.ylim(0.0, 1)
plt.savefig(f'{R}_{ratio}_{abs(A)}.png', format='png')
# plt.show()
