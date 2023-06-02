import os
import numpy as np

import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader
from math import floor


path_to_data = '/home/luishcc/md-projects/sim/radius-scaling/pure-liquid/'


R = 6
ratio = 48

A = 40
grid = 1.0

surf_con = 2.6

n_sim=1

# data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n_sim}'
# data_case_dir = f'R{R}_ratio{ratio}_A{A}/{n_sim}'
# data_case_dir = f'R{R}-{surf_con}/{n_sim}'

data_case_dir = f'{n_sim}'

dir = path_to_data + data_case_dir

# file = 'pinch_A40.lammpstrj'
file = 'pinch_A80.lammpstrj'


datafile = '/'.join([dir,file])


def check_snap(snap, trj):
    trj.read_snapshot_at2(snap)
    data = trj.snap

    length_z = data.box.get_length_z()
    num_z = round(length_z / grid)
    size_z = length_z / (num_z)
    print(length_z, num_z, size_z, num_z*size_z)

    length_x = data.box.get_length_x()
    num_x = round(length_x / 2)
    size_x = length_x / (num_x)

    #temp = []
    bin_count = {id:0 for id in range(num_z+1)}
    #print(    bin_count.keys())

    for atom in data.atoms.values():
        x = atom.position[0]
        y = atom.position[1]
        z = atom.position[2]
        r = np.sqrt(x**2+y**2)
        idz = int(floor( abs(z) / size_z))
        idr_inv = int(floor(3/r))
        #temp.append(idz)
        # print(atom.position, idz)
        bin_count[idz] += idr_inv
    #print(set(temp))
    #print(len(set(temp)), len(bin_count.keys()))
    del bin_count[num_z]
    #del data
    return all(bin_count.values())


def check_file(_file):
    trj = DumpReader(_file)
    trj.map_snapshot_in_file2()
    trj.start_read()

    times = list(trj.timesteps2.keys())
    times.sort()

    n = len(times)
    a = 10
    b = n-10
    fa = check_snap(times[a], trj)
    fb = check_snap(times[b], trj)

    MAX = 1000
    N = 0
    while N < MAX:
        print(N)
        N+=1
        c = (b + a) // 2

        fc = check_snap(times[c], trj)

        print(a, fa, b, fb, c, fc)

        if c == a or c == b:
            print('a: ', a, 'b: ', b)
            break

        if fc == fa:
            a = c
        else:
            b = c

    trj.close_read()
    del trj
    return a


while os.path.isdir(dir):

    print(dir)

    a = check_file(dir + f'/{file}')

    with open(dir+'/breaktime.txt', 'w') as fd:
        fd.write(str(a))

    n_sim += 1
    data_case_dir = f'{n_sim}'


    dir = path_to_data + data_case_dir
