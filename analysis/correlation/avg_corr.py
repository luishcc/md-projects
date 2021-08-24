import sys
import os

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat


path_to_save = os.getcwd()
path_to_data = '/home/luishcc/hdd/free_thread_results/'


R = 10
ratio = 6
sim_case = f'R{R}_ratio{ratio}_A50'

dir_in = path_to_data + sim_case + '-1'
dir_out = '/'.join([path_to_save, sim_case])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

def dict_to_np(dict):
    col = len(dict)
    row = len(dict['dz'])
    data = np.zeros((row, col))
    data[:, 0] = dict['dz']
    for i in range(1, col):
        data[:, i] = dict[str(i-1)]
    return data


def run_snap(dirf, s):
    datfile = dirf + f'/correlation_grid1/{s}.dat'
    data = read_dat(datfile)
    data = dict_to_np(data)
    avg = np.copy(data)
    n = 2
    dirf = '-'.join([dirf.split('-')[0], str(n)])
    datfile = dirf + f'/correlation_grid1/{s}.dat'
    # print(datfile)
    while os.path.isfile(datfile):
        # print(datfile)
        data = read_dat(datfile)
        avg += dict_to_np(data)
        n += 1
        dirf = '-'.join([dirf.split('-')[0], str(n)])
        datfile = dirf + f'/correlation_grid1/{s}.dat'
    return avg / n

DIR = dir_in +'/correlation_grid1/'
onlyfiles = next(os.walk(DIR))[2]
num = len(onlyfiles)

with open(DIR+'0.dat') as f:
    labels = f.readline()
    # print(labels)
    labels = ' '.join(labels.split()[1:])
    # print(labels)
# exit()

for s in range(num):
    print(s)
    corr = run_snap(dir_in, s)
    corr_dat = Dat(corr, labels=labels)
    corr_dat.write_file(f'{s}', dir=dir_out)
