import os
import numpy as np

import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader


file = 'thread.lammpstrj'

trj = DumpReader(file)
trj.map_snapshot_in_file()

times = list(trj.timesteps.keys())
times.sort()

grid = 1.2

def check_snap(snap):
    trj.read_snapshot_at(snap)
    data = trj.snapshots[snap]

    length_z = data.box.get_length_z()
    num_z = round(length_z / grid)
    size_z = length_z / (num_z)

    bin_count = {id:0 for id in range(num_z)}

    for atom in data.atoms.values():
        z = atom.position[2]
        idz = z // grid
        # print(atom.position, idz)
        bin_count[idz] += 1

    return all(bin_count.values())

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

    print(a,b,c)

    if c == a or c == b:
        print('a: ', a, 'b: ', b)
        break

    fc = check_snap(times[c])

    if fc == fa:
        a = c
    else:
        b = c
