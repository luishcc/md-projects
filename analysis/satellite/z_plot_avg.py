import sys
import os
from math import floor, ceil

import numpy as np
from scipy.sparse import coo_matrix

import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid

from scipy.signal import savgol_filter
from scipy.fft import rfft, rfftfreq

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

# dir = '/home/luishcc/hdd/satellite_results'

dir = os.getcwd()

velocity_file = 'dump.vel_14_50_2'
trj_file = 'thread_14_50_2.lammpstrj'

grid = 1.5

trj = DumpReader('/'.join([dir, trj_file]))
trj.read_sequential()

begin_snap = 300
end_snap = 500

num_r = 6
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

    np.savetxt(f'csv_50_2/coor-{trj.snap.time}.csv', coor, delimiter=',')
    np.savetxt(f'csv_50_2/cooz-{trj.snap.time}.csv', cooz, delimiter=',')

    # filter = 20
    # vr = savgol_filter(coo1[:,0], filter, 2, axis=0)
    # vr2 = savgol_filter(coo1[:,1], filter, 2, axis=0)
    # vz = savgol_filter(coo2[:,0], filter, 2, axis=0)
    # vz2 = savgol_filter(coo2[:,1], filter, 2, axis=0)

    fig, ax2 = plt.subplots(nrows=1, ncols=1)

    nn = coor.shape[1]
    # try:
    #     ax1.plot(np.linspace(1, nn, nn), coor.tolist()[2], 'k-', label=r'$r=0$')
    #     # ax1.plot(np.linspace(1, nn, nn), coor.tolist()[-1], label=r'$r=1$')
    # except Exception as e: print(e)
    # # ax1.legend(loc='lower right')
    # ax1.set_title(r'$v_r$')

    try:
        ax2.plot(np.linspace(1, nn, nn), cooz.tolist()[1], 'k-', label=r'$r=0$')
        # ax2.plot(np.linspace(1, nn, nn), cooz.tolist()[-1], label=r'$r=1$')
    except Exception as e: print(e)
    # ax2.legend(loc='lower right')
    ax2.set_ylabel(r'$v_z$')
    ax2.set_xlabel(r'$L$')
    ax2.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)


    # plt.show()
    # continue

    if end:
        plt.show()
        break
    if not end:
        plt.savefig(f'f2_50_2/{trj.snap.time}.png', dpi=250)
        plt.close()
