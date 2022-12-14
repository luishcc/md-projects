import sys
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mdpkg.rwfile import read_dat, Dat

path_to_save = os.getcwd()
path_to_data = '/home/luishcc/hdd/free_thread_results/'
# path_to_data = '/home/luishcc/hdd/'

# path_to_data = '/media/luis/luis-backup/hdd1-panos3/hdd/free_thread_results/'
# path_to_data = '/home/luishcc/test/'

R = 4
ratio = 48
A = -50

initial = 0
final = 600

sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'

dir_in = path_to_data + sim_case
dir_out = '/'.join([path_to_save, sim_case])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

os.chdir(dir_out)

def path_to_file(case, snap):
    return dir_in + '-' + str(case) + f'/cluster/{snap}.csv'

def run_snap(_snap):
    case = 1
    file_list = []
    ff = path_to_file(case, _snap)
    while os.path.isfile(ff):
        file_list.append(ff)
        case += 1
        ff = path_to_file(case, _snap)

    try:
        combined_csv = pd.concat([pd.read_csv(f) for f in file_list ])
        combined_csv.to_csv(f'{_snap}.csv', index=False)
    except:
        return

for s in range(initial, final+1):
    print(s)
    run_snap(s)
