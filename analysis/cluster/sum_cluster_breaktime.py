import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat

path_to_save = os.getcwd()
# path_to_data = '/home/luishcc/hdd/free_thread_results/'
path_to_data = '/home/luishcc/hdd/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'

# path_to_data = '/media/luis/luis-backup/hdd1-panos3/hdd/free_thread_results/'
# path_to_data = '/home/luishcc/test/'

def get_snap(dir):
    with open(dir+'/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

R = 4
ratio = 48
A = -90

sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'

dir_in = path_to_data + sim_case

# sim_case2 = f'R{R}_ratio{ratio}_A{abs(A+1)}'

dir_out = '/'.join([path_to_save, sim_case])
if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

os.chdir(dir_out)

def path_to_file(case, snap):
    return dir_in + '/' + str(case) + f'/cluster/{snap}.csv'

def run_snap(n, break_lst):
    file_list = []
    for i, break_t in enumerate(break_lst):
        _snap = break_t + n
        ff = path_to_file(i+1, _snap)
        file_list.append(ff)
    try:
        combined_csv = pd.concat([pd.read_csv(f) for f in file_list ])
        combined_csv.to_csv(f'{n}.csv', index=False)
    except Exception as e:
        print(e)
        return

list_times = []
case = 1
ff = dir_in + '/' + str(case)
while os.path.isdir(ff):
    list_times.append(get_snap(ff))
    case += 1
    ff = dir_in + '/' + str(case)

for i in range(600):
    print(i)
    run_snap(i, list_times)
