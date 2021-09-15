import sys
import os
from math import floor, ceil

import numpy as np
from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq
import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid


path_to_data = '/home/luishcc/hdd/free_thread_results/'

R = 6
ratio = 12
A = 50
grid = 0.5

n = 1
data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
dir = path_to_data + data_case_dir
save_fourier_dir = dir + f'/fourier_grid{grid}'
save_correlation_dir = dir + f'/correlation_grid{grid}'


size = 1
rrange = ceil((R*1.7)/size)

list = [str(r) for r in range(rrange)]
header_c = 'dz ' + ' '.join(list)
header_f = 'freq ' + ' '.join(list)



def run_case(n, iter, skip):
    while True:
        print(iter)
        grd = Grid(trj.snap, size=grid)
        num = floor(grd.num_z/2)
        dz = np.linspace(0, grd.length_z/2, num)

        if num % 2 == 0:
            num_f = int((num / 2) + 1)
        else:
            num_f = int((num + 1) / 2)

        corr = np.empty((num, rrange+1))
        corr[:] = np.NaN
        # fourier = np.empty((num_f, rrange+1), dtype='complex')
        # fourier[:] = np.NaN
        # freq = rfftfreq(num)
        corr[:, 0] = dz
        # fourier[:, 0] = freq
        for r in range(rrange):
            a = grd.compute_density_correlation(r)
            # if float('Nan') in a:
            if np.any(np.isnan(a)):
                # continue
                break
            # f = rfft(a) / num
            for i in range(num):
                corr[i, r+1] = a[i]
            #     try:
            #         fourier[i, r+1] = f[i]
            #     except:
            #         continue

        corr_dat = Dat(corr, labels=header_c)
        # rfft_dat = Dat(fourier, labels=header_f)

        corr_dat.write_file(f'{iter}', dir=save_correlation_dir)
        # rfft_dat.write_file(f'{iter}', dir=save_fourier_dir)

        try:
            trj.skip_next(skip)
            trj.read_next()
            iter += (skip + 1)
        except:
            trj.close_read()
            break

while os.path.isdir(dir):
    print(dir)
    trj = DumpReader(dir + '/thread.lammpstrj')
    trj.read_sequential()
    iter = 0
    skip = 0
    run_case(n, iter, skip)
    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
    dir = path_to_data + data_case_dir
    # save_fourier_dir = dir + f'/fourier_grid{grid}'
    save_correlation_dir = dir + f'/correlation_grid{grid}'
