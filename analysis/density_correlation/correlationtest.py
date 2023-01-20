import sys
import os
from math import floor, ceil

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid


path_to_data = '/home/luishcc/hdd/free_thread_old/'
# path_to_data = '/home/luishcc/hdd/'


R = 6
ratio = 48
A = 50
grid = 1

max = 600
skip = 0

n = 1 + 10*0
nn = n + 100
data_case_dir = f'R{R}_ratio{ratio}_A{A}/{n}'
dir = path_to_data + data_case_dir
save_correlation_dir = dir + f'/correlation_grid{grid}'


size = 1
rrange = ceil((R*1.7)/size)
rrange = ceil((1))

list = [str(r) for r in range(rrange)]
header_c = 'dz ' + ' '.join(list)
header_f = 'freq ' + ' '.join(list)


def run_case(n, iter, skip, max):
    while True:
        if trj.snap.time != 16300:
            print(trj.snap.time)
            iter += (skip + 1)
            if iter >= max:
                break
            trj.skip_next(162)
            trj.read_next()
            continue
        else:
            print(trj.snap.time, '  --  run!!')

        print(iter)
        grd = Grid(trj.snap, size=grid)
        num = floor(grd.num_z/2)
        dz = np.linspace(0, grd.length_z/2, num)

        corr = np.empty((num, rrange+1))
        corr[:] = np.NaN
        corr[:, 0] = dz

        for r in range(rrange):
            print(r, '1')
            a = grd.compute_density_correlation(4)
            if np.any(np.isnan(a)):
                break

            print(r, '1')
            for i in range(num):
                corr[i, r+1] = a[i]

        corr_dat = Dat(corr, labels=header_c)
        # corr_dat.write_file(f'{iter}', dir=save_correlation_dir)
        corr_dat.write_file(f'test', dir=dir)

        try:
            iter += (skip + 1)
            if iter >= max:
                break
            trj.skip_next(skip)
            trj.read_next()
        except:
            trj.close_read()
            break
print('reading')
trj = DumpReader(dir + '/thread.lammpstrj')
print('reading')
trj.read_sequential()
print('running')
run_case(0, 0, 0, 500)
