import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


R = 6
R2 = 5
ratio = 48
A = -50
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

def get_max(x, y, ran):
    id = y.index(max(y))
    print(id)
    y = y[id-ran:id+ran+1]
    x = x[id-ran:id+ran+1]
    fit = np.polyfit(x,y,2)
    return -fit[1]/(2*fit[0])

import matplotlib
def color(r,l):
    cmap = matplotlib.cm.get_cmap('Spectral')
    # return cmap(r/l)
    return 'black'


from_freq = 3
snap = 0
file = dir + f'/{snap}.dat'
plt.figure(1)
while os.path.isfile(file) and snap < 500:
    print(file)
    data = read_dat(file)

    col = len(data)
    max_freq = 0
    sum = 0
    for i in range(4,7):
        try:
            # print(data[str(i-1)][from_freq:])
            max_freq += get_max(data['freq'][from_freq:],
                                data[str(i-1)][from_freq:], 1)
            print(max_freq)
            sum += 1
        except TypeError:
            print('skipped  ', i)
            continue
    try:
        plt.scatter(snap, 2*np.pi*R2*max_freq/sum,
                edgecolors=color(i,col), facecolors=color(i,col))
    except ZeroDivisionError:
        pass
    snap += 1
    file = dir + f'/{snap}.dat'


plt.xlabel(r'Time')
plt.ylabel(r'reduced wavenumber')
plt.title(f'R = {R}, Ratio = {ratio}, A = {A}')
plt.grid(True)
plt.ylim(0.0, 1)
plt.savefig(f'{R}_{ratio}_{abs(A)}_fit.png', format='png')
# plt.show()
