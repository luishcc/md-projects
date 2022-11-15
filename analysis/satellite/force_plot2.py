import sys
import os
from math import floor, ceil

import numpy as np
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid

from scipy.signal import savgol_filter
from scipy.fft import rfft, rfftfreq

# dir = '/home/luishcc/testdata'
# dir = '/home/luishcc/md-projects/tests/rerun'
dir = os.getcwd()

# force_file = 'dump.force'
velocity_file = 'dump.vel_14_80'
trj_file = 'thread_14_80.lammpstrj'



grid = 1.5

trj = DumpReader('/'.join([dir, trj_file]))
trj.read_sequential()


# trj.read_next()
# trj.read_force('/'.join([dir, force_file]), trj.snap)
# grd = Grid(trj.snap, size = grid)
# print(trj.snap.time)

def run2():

    idr = []
    idz = []
    d = [[], [], [], []]
    for key, cell in grd.cell.items():
        if cell.id[0] not in [0,4]:
            print(cell.id[0])
            continue
        idr.append(cell.id[0])
        idz.append(cell.id[2])
        # force = cell.get_force_cylindrical()
        vel = cell.get_velocity_cylindrical()
        # d[0].append(force[0]/cell.nangle)
        # d[1].append(force[2]/cell.nangle)
        d[2].append(vel[0]/cell.nangle)
        d[3].append(vel[2]/cell.nangle)

    coo = coo_matrix((d[2], (idr, idz)))
    coo0 = coo_matrix((d[2], (idr, idz)))
    coo1 = coo_matrix((d[2], (idr, idz)))
    coo2 = coo_matrix((d[3], (idr, idz)))
    return coo, coo0, coo1, coo2

print('skipping')
trj.skip_next(464)
end = True
while True:
    try:
        print('reading trj')
        trj.read_next()
        # trj.read_force('/'.join([dir, force_file]), trj.snap)
        trj.read_velocity('/'.join([dir, velocity_file]), trj.snap)
        print('making coo matrix')
        grd = Grid(trj.snap, size = grid)
        print(trj.snap.time)
        coo, coo0, coo1, coo2 = run2()
    except Exception as e:
        print(e)
        break

    coo = coo.todense().transpose()
    coo0 = coo0.todense().transpose()
    coo1 = coo1.todense().transpose()
    coo2 = coo2.todense().transpose()

    np.savetxt(f'csv/coo.csv', coo, delimiter=',')


    filter = 20
    fr = savgol_filter(coo[:,0], filter, 2, axis=0)
    fr2 = savgol_filter(coo[:,1], filter, 2, axis=0)
    fz = savgol_filter(coo0[:,0], filter, 2, axis=0)
    fz2 = savgol_filter(coo0[:,1], filter, 2, axis=0)
    vr = savgol_filter(coo1[:,0], filter, 2, axis=0)
    vr2 = savgol_filter(coo1[:,1], filter, 2, axis=0)
    vz = savgol_filter(coo2[:,0], filter, 2, axis=0)
    vz2 = savgol_filter(coo2[:,1], filter, 2, axis=0)

    # freq = rfftfreq(len(coo))
    # fr = rfft(coo[:,0], axis=0)
    # fr2 = rfft(coo[:,1], axis=0)
    # fz = rfft(coo0[:,0], axis=0)
    # fz2 = rfft(coo0[:,1], axis=0)
    # vr = rfft(coo1[:,0], axis=0)
    # vr2 = rfft(coo1[:,1], axis=0)
    # vz = rfft(coo2[:,0], axis=0)
    # vz2 = rfft(coo2[:,1], axis=0)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(15,9))
    # fig, ax1 = plt.subplots(nrows=1, ncols=1)

    try:
        ax1.plot(np.linspace(1, len(coo), len(coo)), coo[:,0], label='0')
        ax1.plot(np.linspace(1, len(coo), len(coo)), coo[:,1], label='1')
        # ax1.plot(np.linspace(1, len(coo), len(coo)), fr, label='4')
        # ax1.plot(np.linspace(1, len(coo), len(coo)), fr2, label='3')
        # ax1.plot(freq, fr, label='4')
        # ax1.plot(freq, fr2, label='3')
    except Exception as e: print(e)
    ax1.legend(loc='lower right')
    ax1.set_title(r'$F_r$')
    # ax1.set_xlabel('ID_z')
    # ax1.set_ylim(-20, 10)
    # ax1.set_ylabel('Force')

    try:
        ax2.plot(np.linspace(1, len(coo0), len(coo0)), coo0[:,0], label='4')
        ax2.plot(np.linspace(1, len(coo0), len(coo0)), coo0[:,1], label='3')
        # ax2.plot(np.linspace(1, len(coo0), len(coo0)), fz, label='4')
        # ax2.plot(np.linspace(1, len(coo0), len(coo0)), fz2, label='3')
        # ax2.plot(freq, fz, label='4')
        # ax2.plot(freq, fz2, label='3')
    except Exception as e: print(e)
    ax2.legend(loc='lower right')
    ax2.set_title(r'$F_z$')
    # ax2.set_xlabel('ID_z')
    # ax2.set_ylim(-15, 15)
    # ax2.set_ylabel('Force')

    try:
        ax3.plot(np.linspace(1, len(coo1), len(coo1)), coo1[:,0], label='4')
        ax3.plot(np.linspace(1, len(coo1), len(coo1)), coo1[:,1], label='3')
        # ax3.plot(np.linspace(1, len(coo1), len(coo1)), vr, label='4')
        # ax3.plot(np.linspace(1, len(coo1), len(coo1)), vr2, label='3')
        # ax3.plot(freq, vr, label='4')
        # ax3.plot(freq, vr2, label='3')
    except Exception as e: print(e)
    ax3.legend(loc='lower right')
    ax3.set_title(r'$V_r$')
    # ax3.set_xlabel('ID_z')
    # ax3.set_ylim(-0.4, 0.4)
    # ax3.set_ylabel('Force')

    try:
        ax4.plot(np.linspace(1, len(coo2), len(coo2)), coo2[:,0], label='4')
        ax4.plot(np.linspace(1, len(coo2), len(coo2)), coo2[:,1], label='3')
        # ax4.plot(np.linspace(1, len(coo2), len(coo2)), vz, label='4')
        # ax4.plot(np.linspace(1, len(coo2), len(coo2)), vz2, label='3')
        # ax4.plot(freq, vz, label='4')
        # ax4.plot(freq, vz2, label='3')
    except Exception as e: print(e)
    ax4.legend(loc='lower right')
    ax4.set_title(r'$V_z$')
    ax4.tick_params(axis='x', which='both', bottom=False,
                    top=False, labelbottom=False)

    # ax4.set_xlabel('ID_z')
    # ax4.set_ylim(-0.3, 0.3)
    # ax4.set_ylabel('Force')


    plt.show()
    continue

    if end:
        plt.show()
        break
    if not end:
        plt.savefig(f'f2/{trj.snap.time}.png', dpi=250)
        plt.close()
