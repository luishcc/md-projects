import sys
import os
from math import floor, ceil

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid



dir = '/home/luishcc/testdata'
dir = '/home/luishcc/md-projects/tests/rerun'


velocity_file = 'dump.vel2'
force_file = 'dump.force2'
trj_file = 'thread2.lammpstrj'

velocity_file = 'dump.vel'
force_file = 'dump.force'
trj_file = 'thread.lammpstrj'

# velocity_file = 'dump.vel3'
# force_file = 'dump.force3'
# trj_file = 'thread3.lammpstrj'


save_dir = trj_file.split('.')[0]


grid = 1.5

R = 6
# ratio = 48
# A = 50
# grid = 1
#
max = 150
skip = 5
#
# n = 1 + 10*0
# nn = n + 100
# data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
# dir = path_to_data + data_case_dir
# save_correlation_dir = dir + f'/correlation_grid{grid}'


size = grid
rrange = 5

list = [str(r) for r in range(5)]
header_c = 'dz ' + ' '.join(list)


def run_case(iter, skip, max):
    while True:
        print(iter)
        grd = Grid(trj.snap, size=grid)
        num = floor(grd.num_z/2)
        dz = np.linspace(0, grd.length_z/2, num)

        corr = np.empty((num, rrange+1))
        corr[:] = np.NaN
        corr[:, 0] = dz

        for r in range(rrange):
            # grd.set_forces()
            # grd.set_velocities()
            # a = grd.compute_auto_correlation(r, ['density', 'density'])
            a = grd.compute_density_correlation(r)
            if np.any(np.isnan(a)):
                break

            for i in range(num):
                corr[i, r+1] = a[i]

        corr_dat = Dat(corr, labels=header_c)
        # corr_dat.write_file(f'{iter}', dir=save_dir+'/force')
        corr_dat.write_file(f'{iter}', dir=save_dir+'/cross')
        # corr_dat.write_file(f'{iter}', dir=save_dir+'/velocity')
        # corr_dat.write_file(f'{iter}', dir=save_dir+'/density')

        try:
            iter += (skip + 1)
            if iter >= max:
                break
            trj.skip_next(skip)
            trj.read_next()
            # trj.read_force('/'.join([dir,force_file]), trj.snap)
            # trj.read_velocity('/'.join([dir,velocity_file]), trj.snap)
        except Exception as e:
            trj.close_read()
            print(e)
            break


trj = DumpReader('/'.join([dir,trj_file]))
trj.read_sequential()
trj.skip_next(0)
# trj.read_force('/'.join([dir,force_file]), trj.snap)
# trj.read_velocity('/'.join([dir,velocity_file]), trj.snap)
iter = 0
grd = run_case(iter, skip, max)
exit()

# while os.path.isdir(dir):
#     print(dir)
    # if os.path.isdir(save_correlation_dir):
    #     n+=1
    #     data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
    #     dir = path_to_data + data_case_dir
    #     save_correlation_dir = dir + f'/correlation_grid{grid}'
    #     continue
    # trj = DumpReader(trj_file)
    # trj.read_sequential()
    # iter = 0
    # run_case(n, iter, skip, max)
    # n += 1
    # if n >= nn:
    #     exit()
    # data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
    # dir = path_to_data + data_case_dir
    # save_correlation_dir = dir + f'/correlation_grid{grid}'
