import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat

path_to_save = os.getcwd()
path_to_data = '/home/luishcc/hdd/free_thread_results/'
path_to_data = '/home/luishcc/hdd/'
# path_to_data = '/media/luis/luis-backup/hdd1-panos3/hdd/free_thread_results/'
# path_to_data = '/home/luishcc/test/'

def get_snap(dir):
    with open(dir+'/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

R = 2
ratio = 48
A = -85

snap_time_t = 31
snap_time_s = 15

separation = 1.7

sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'

dir_in = path_to_data + sim_case

def path_to_file_t(case, snap):
    return dir_in + '-' + str(case) + f'/cluster/{snap+snap_time_t}.csv'

def path_to_file_s(case, snap):
    return dir_in + '-' + str(case) + f'/cluster/{snap+snap_time_s}.csv'


case = 1
ff = dir_in + '-' + str(case)

sum = 0
sumsq = 0
n = 0

while os.path.isdir(ff):
    ss = get_snap(ff)
    file_t = path_to_file_t(case, ss)
    file_s = path_to_file_s(case, ss)

    df = pd.read_csv(file_t)
    df2 = pd.read_csv(file_s)

    df.drop(df[df['size'] <= 1].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)

    df2.drop(df[df['size'] <= 1].index, inplace=True)
    df2.drop(df[df['anisotropy'] > 0.2].index, inplace=True)

    satellite = df[df['radius'] < separation]

    num_total = df.shape[0] / (2*np.pi*4.8)
    num_satellite = satellite.shape[0] / (2*np.pi*4.8)

    sum += num_satellite/num_total
    sumsq += (num_satellite/num_total)**2
    n += 1

    case += 1
    ff = dir_in + '-' + str(case)

avg = sum/n
std = sumsq/n - avg**2
print( avg, std, n)
