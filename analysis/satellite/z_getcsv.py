import sys
import os
from math import floor, ceil

import numpy as np
from scipy.sparse import coo_matrix

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid


# dir = '/home/luishcc/testdata'
# dir = '/home/luishcc/md-projects/tests/rerun'
#
# # force_file = 'force.test'
# # trj_file = 'test.lammpstrj'
# #
# # force_file = 'dump.force2'
# # velocity_file = 'dump.vel2'
# # trj_file = 'thread2.lammpstrj'
# #
# force_file = 'dump.force'
# velocity_file = 'dump.vel'
# trj_file = 'thread.lammpstrj'

dir = '/home/luishcc/hdd/satellite_results'

# dir = os.getcwd()

velocity_file = 'dump.vel_14_80'
trj_file = 'thread_14_80.lammpstrj'

grid = 1.2

trj = DumpReader('/'.join([dir, trj_file]))
trj.read_sequential()

begin_snap = 400
end_snap = 550

num_r = 8
def run2():
    idr = []
    idz = []
    d = [[], []]
    for key, cell in grd.cell.items():
        if cell.id[0] >= num_r :
            continue
        idr.append(cell.id[0])
        idz.append(cell.id[2])
        vel = cell.get_velocity_cylindrical()
        d[0].append(vel[0]/cell.nangle)
        d[1].append(vel[2]/cell.nangle)
    coor = coo_matrix((d[0], (idr, idz)))
    cooz = coo_matrix((d[1], (idr, idz)))
    return coor, cooz

print('skipping')
trj.skip_next(begin_snap)
end = False
count = 0
while count + begin_snap < end_snap:

    try:
        lst = []
        len_coo = []
        for i in range(4):
            count += 1
            print('reading ', i)
            trj.read_next()
            print('reading vel ', i)
            trj.read_velocity('/'.join([dir, velocity_file]), trj.snap)
            grd = Grid(trj.snap, size = grid)
            # print(trj.snap.time)

            coor, cooz = run2()
            coor = coor.todense()
            cooz = cooz.todense()

            lst.append([coor, cooz])
            len_coo.append(coor.shape[1])

    except Exception as e:
        print(e)
        break

    print('plotting')
    nn = min(len_coo)
    coor = (lst[0][0][:,:nn] + lst[1][0][:,:nn] + lst[2][0][:,:nn] + lst[3][0][:,:nn])/4
    cooz = (lst[0][1][:,:nn] + lst[1][1][:,:nn] + lst[2][1][:,:nn] + lst[3][1][:,:nn])/4

    np.savetxt(f'csv_80_long/coor-{trj.snap.time}.csv', coor, delimiter=',')
    np.savetxt(f'csv_80_long/cooz-{trj.snap.time}.csv', cooz, delimiter=',')



    if end:
        break
