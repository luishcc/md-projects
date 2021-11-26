import sys
import os
from math import floor, ceil

import numpy as np
import matplotlib.pyplot as plt

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid


dir = '/home/luishcc/testdata'

force_file = 'force.test'
trj_file = 'test.lammpstrj'

# force_file = 'dump.force'
# trj_file = 'thread.lammpstrj'

grid = 1

# def plot(n):
#     plt.figure(n)
#     plt.


def run_case():
    iter = 0
    while True:
        print(iter)
        grd = Grid(trj.snap, size=grid)
        num = floor(grd.num_z/2)

        try:
            iter += 1
            trj.read_next()
        except:
            trj.close_read()
            break

trj = DumpReader('/'.join([dir, trj_file]))
trj.read_sequential()

trj.read_next()
trj.read_force('/'.join([dir, force_file]), trj.snap)
print()



# run_case(n, iter, skip, max)
