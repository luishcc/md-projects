import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat

R = 8
ratio = 48
A = -50

try:
    surf_con = float(sys.argv[1])
except IndexError:
    surf_con = 1.0

snap_time_t = 163
snap_time_s = 94

separation = 8

path_to_save = os.getcwd()
path_to_data = '/home/luishcc/hdd/free_thread_results/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
path_to_data = '/home/luishcc/hdd/'
# path_to_data = '/media/luis/luis-backup/hdd1-panos3/hdd/free_thread_results/'
# path_to_data = '/home/luishcc/test/'

path_to_data = '/home/luishcc/hdd/surfactant/new/'

def get_snap(dir):
    with open(dir+'/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

# sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'
sim_case = f'R{R}-{surf_con}'

dir_in = path_to_data + sim_case

def path_to_file_t(case, snap):
    # return dir_in + '-' + str(case) + f'/cluster/{snap+snap_time_t}.csv'
    return dir_in + '/' + str(case) + f'/cluster/{snap+snap_time_t}.csv'


def path_to_file_s(case, snap):
    # return dir_in + '-' + str(case) + f'/cluster/{snap+snap_time_s}.csv'
    return dir_in + '/' + str(case) + f'/cluster/{snap+snap_time_s}.csv'


case = 1
ff = dir_in + '-' + str(case)
ff = dir_in + '/' + str(case)

sum = 0
sumsq = 0
n = 0

print(ff)

while os.path.isdir(ff):
    ss = get_snap(ff)
    file_t = path_to_file_t(case, ss)
    file_s = path_to_file_s(case, ss)

    df = pd.read_csv(file_t)
    df2 = pd.read_csv(file_s)

    df.drop(df[df['size'] <= 8].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.25].index, inplace=True)

    df2.drop(df2[df2['size'] <= 6].index, inplace=True)
    df2.drop(df2[df2['anisotropy'] > 0.25].index, inplace=True)

    satellite = df2[df2['radius'] < separation]
    main = df[df['radius'] > separation]


    num_total = df.shape[0]
    # num_total = main.shape[0]
    num_satellite = satellite.shape[0]

    sum += num_satellite/num_total
    sumsq += (num_satellite/num_total)**2
    n += 1

    case += 1
    # ff = dir_in + '-' + str(case)
    ff = dir_in + '/' + str(case)


avg = sum/n
std = sumsq/n - avg**2
print("Avg: ", avg, "Var: ", std, "N: ", n)
