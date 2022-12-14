from ovito.io import *
from ovito.modifiers import *

from scipy.linalg import eig, inv
import numpy as np

from mdpkg.rwfile import Dat, CSV

import os


from mdpkg.rwfile import read_dat, Dat


# dir = '/home/luishcc/hdd/free_thread_results/R6_ratio6_A50-4/'
file = '/thread.lammpstrj'

path_to_data = '/home/luishcc/hdd/free_thread_results/'
# path_to_data = '/home/luishcc/hdd/'
# path_to_data = '/home/luishcc/test/'


R = 6
ratio = 48
A = -60

initial_snap = 0
final_step = 600


n = 1
data_case_dir = f'R{R}_ratio{ratio}_A{abs(A)}-{n}'

dir = path_to_data + data_case_dir
save_dir = dir + f'/cluster'


def asphericity(lst):
    return abs(lst[2] - 0.5 * (lst[0]+lst[1]))

def anisotropy(lst):
    n = (lst[0]**2+lst[1]**2+lst[2]**2)
    d = (lst[0]+lst[1]+lst[2])**2
    return abs(1.5 * n / d - 0.5)

def acylindricity(lst):
    return abs(lst[1] - lst[0])

def get_eig(d):
    gy = np.array([[d[0], d[3], d[4]],
                   [d[3], d[1], d[5]],
                   [d[4], d[5], d[2]]])
    eva, eve = eig(gy)
    eva.sort()
    return eva

labels = ['size', 'radius', 'asphericity', 'acylindricity', 'anisotropy']

while os.path.isdir(dir):

    print(dir)

    # if os.path.isdir(save_dir):
    #     n += 1
    #     data_case_dir = f'R{R}_ratio{ratio}_A{abs(A)}-{n}'
    #     dir = path_to_data + data_case_dir
    #     save_dir = dir + f'/cluster'
    #     continue

    pipeline = import_file(dir+file)

    clt_mod = ClusterAnalysisModifier(cutoff = 0.8, compute_gyration = True)
    pipeline.modifiers.append(clt_mod)

    for i in range(initial_snap, pipeline.source.num_frames):
        if i >= final_step:
            break
        data = pipeline.compute(i)
        cluster_table = data.tables['clusters']
        print(i)

        a = cluster_table['Radius of Gyration'][...]
        b = cluster_table['Cluster Size'][...]
        c = cluster_table['Gyration Tensor'][...]

        ncl = len(a)
        table = np.zeros((ncl, 5))

        for j in range(ncl):
            table[j, 0] = b[j]
            table[j, 1] = a[j]
            ev = get_eig(c[j])
            table[j, 2] = asphericity(ev)
            table[j, 3] = acylindricity(ev)
            table[j, 4] = anisotropy(ev)

        save = CSV(table, labels)
        save.write_file(f'{i}', dir=save_dir)

        # print(a, '\n', b, '\n', c)
        # print()

    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{abs(A)}-{n}'
    dir = path_to_data + data_case_dir
    save_dir = dir + f'/cluster'


# export_file(pipeline, f'{i}.dat', 'txt/table', key='clusters')
# pandas.read_csv('dat', sep=' ', header=0, names=[labels])
