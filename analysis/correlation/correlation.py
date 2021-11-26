import sys
import os
from math import floor, ceil

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid


# path_to_data = '/home/luishcc/hdd/free_thread_results/'
path_to_data = '/home/luishcc/hdd/'


R = 6
ratio = 48
A = 85
grid = 1

max = 600
skip = 0

n = 1 + 10*0
nn = n + 10
data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
dir = path_to_data + data_case_dir
save_correlation_dir = dir + f'/correlation_grid{grid}'


size = 1
rrange = ceil((R*1.7)/size)

list = [str(r) for r in range(rrange)]
header_c = 'dz ' + ' '.join(list)
header_f = 'freq ' + ' '.join(list)


def run_case(n, iter, skip, max):
    while True:
        print(iter)
        grd = Grid(trj.snap, size=grid)
        num = floor(grd.num_z/2)
        dz = np.linspace(0, grd.length_z/2, num)

        corr = np.empty((num, rrange+1))
        corr[:] = np.NaN
        corr[:, 0] = dz

        for r in range(rrange):
            a = grd.compute_density_correlation(r)
            if np.any(np.isnan(a)):
                break

            for i in range(num):
                corr[i, r+1] = a[i]

        corr_dat = Dat(corr, labels=header_c)
        corr_dat.write_file(f'{iter}', dir=save_correlation_dir)

        try:
            iter += (skip + 1)
            if iter >= max:
                break
            trj.skip_next(skip)
            trj.read_next()
        except:
            trj.close_read()
            break

while os.path.isdir(dir):
    print(dir)
    trj = DumpReader(dir + '/thread.lammpstrj')
    trj.read_sequential()
    iter = 0
    run_case(n, iter, skip, max)
    n += 1
    if n >= nn:
        exit()
    data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
    dir = path_to_data + data_case_dir
    save_correlation_dir = dir + f'/correlation_grid{grid}'
