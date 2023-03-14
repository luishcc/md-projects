import sys
import os
from math import floor, ceil

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader, CSV, Dat
from mdpkg.grid import Gridz, Grid


# path_to_data = '/home/luishcc/hdd/free_thread_old/'
path_to_data = '/home/luishcc/hdd/surfactant/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
# path_to_data = '/home/luishcc/hdd/'
# path_to_data = '/home/luishcc/'

R = 8
ratio = 24
A = 50
grid = 1

surf_con = 2.3

r1 = 6.5
r2 = 9.5

# sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'
sim_case = f'R{R}-{surf_con}'
case = 11
path_to_data = path_to_data + sim_case
dir = path_to_data + '/' + str(case)
save_correlation_file = f'breaktime_correlation_grid{grid}'

print(dir)

def get_snap(dir):
    with open(dir+'/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

header_c = ['dz', 'correlation']
header_c = 'dz correlation'


def run_case():
    grd = Gridz(trj.snap, size=grid, Rlow = r1, Rup = r2)
    # grd = Grid(trj.snap, size=grid)
    num = floor(grd.num_z/2)
    dz = np.linspace(0, grd.length_z/2, num)

    corr = np.empty((num, 2))
    corr[:] = np.NaN
    corr[:, 0] = dz

    corr[:, 1] = grd.compute_density_correlation()

    corr_dat = Dat(corr, labels=header_c)
    corr_dat.write_file(save_correlation_file, dir=dir)


while os.path.isdir(dir):
    print(dir)
    # if os.path.isfile(save_correlation_file):
    #     case += 1
    #     dir = path_to_data +  '/' + str(case)
    #     save_correlation_file = f'breaktime_correlation_grid{grid}'
    #     continue
    # trj = DumpReader(dir + '/thread.lammpstrj')
    trj = DumpReader(dir + f'/cylinder_{R}_{surf_con}.lammpstrj')
    trj.read_sequential()
    # trj.skip_next(get_snap(dir)-1)
    trj.skip_next(get_snap(dir)-2)
    trj.read_next()
    print(trj.snap.time)
    iter = 0
    run_case()
    case += 1
    dir = path_to_data + '/' + str(case)
    save_correlation_file = f'breaktime_correlation_grid{grid}'
