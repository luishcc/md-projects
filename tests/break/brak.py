import os
import numpy as np

import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader


path_to_data = '/home/luishcc/hdd/free_thread_results/'


R = 6
ratio = 12

A = 50
grid = 1.2


n_sim=1

data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n_sim}'
dir = path_to_data + data_case_dir

file = 'thread.lammpstrj'
datafile = '/'.join([dir,file])


def check_snap(snap):
    trj.read_snapshot_at(snap)
    data = trj.snapshots[snap]

    length_z = data.box.get_length_z()
    num_z = round(length_z / grid)
    size_z = length_z / (num_z)

    temp = []
    bin_count = {id:0 for id in range(num_z)}
    print(    bin_count.keys())

    for atom in data.atoms.values():
        z = atom.position[2]
        idz = int( z // grid)
        temp.append(idz)
        #print(atom.position, idz)
        bin_count[idz] += 1
    print(set(temp))
    print(len(set(temp)), len(bin_count.keys()))
    return all(bin_count.values())


def check_file(_file):
    trj = DumpReader(_file)
    trj.map_snapshot_in_file()

    times = list(trj.timesteps.keys())
    times.sort()

    n = len(times)
    a = 0
    b = n-1
    fa = check_snap(times[a])
    fb = check_snap(times[b])

    MAX = 1000
    N = 0
    while N < MAX:
        print(N)
        N+=1
        c = (b + a) // 2

        fc = check_snap(times[c])

        print(a, fa, b, fb, c, fc)

        if c == a or c == b:
            print('a: ', a, 'b: ', b)
            break

        if fc == fa:
            a = c
        else:
            b = c
    return a

while os.path.isdir(dir):

    print(dir)

    a = check_file(dir + '/thread.lammpstrj')
    with open(dir+'breaktime.txt', 'w') as fd:
        fd.write(str(a))

    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n}'
    dir = path_to_data + data_case_dir
