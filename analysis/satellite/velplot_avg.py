import sys
import os
from math import floor, ceil

import numpy as np
from scipy.sparse import coo_matrix
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
# plt.rcParams.update({
#   "text.usetex": True,
#   "font.family": "Helvetica"
# })


from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid


# dir = '/home/luishcc/testdata'
# dir = '/home/luishcc/md-projects/tests/rerun'
#dir = '/home/luis/md-projects/sim/satellite'
dir = '/home/luishcc/hdd/super_download/satellite_A80_l1'

# dir = os.getcwd()


vel_file = 'dump.vel_14_80'
trj_file = 'thread_14_80.lammpstrj'

#
# velocity_file = 'dump.vel'
# trj_file = 'thread.lammpstrj'
#
#
# velocity_file = 'dump.vel3'
# trj_file = 'thread3.lammpstrj'



grid = 1.5

trj = DumpReader('/'.join([dir, trj_file]))
trj.read_sequential()
#
# trj.skip_next(170)
# trj.read_next()
# trj.read_force('/'.join([dir, force_file]), trj.snap)
# grd = Grid(trj.snap, size = grid)
# print(trj.snap.time)

import matplotlib as mpl
cmap = mpl.cm.cool
#norm = mpl.colors.Normalize(vmin=-15, vmax=15)

def run2():

    idr = []
    idz = []
    d = [[], [], []]
    dens = []
    force = [[], []]
    num_r = 12
    for key, cell in grd.cell.items():
        if cell.id[0] >= num_r :
            continue
        idr.append(cell.id[0])
        idz.append(cell.id[2])
        v = cell.get_velocity_cylindrical()
        dens.append(cell.get_density()/cell.nangle)
        d[0].append(v[0]/cell.nangle)
        d[1].append(v[1]/cell.nangle)
        d[2].append(v[2]/cell.nangle)

    idr = [-i + num_r-1 for i in idr]
    coo0 = coo_matrix((d[0], (idr, idz)))
    coo1 = coo_matrix((d[1], (idr, idz)))
    coo2 = coo_matrix((d[2], (idr, idz)))
    return coo0, coo1, coo2

begin_snap = 320
trj.skip_next(begin_snap)
end = False
end_snap = 500

count = 0
while count + begin_snap < end_snap:
    count += 1
    try:
        lst = []
        len_coo = []
        for i in range(4):

            trj.read_next()
            trj.read_velocity('/'.join([dir, vel_file]), trj.snap)
            grd = Grid(trj.snap, size = grid)
            print(trj.snap.time)

            coo0, coo1, coo2 = run2()

            coo0 = coo0.todense()
            coo1 = coo1.todense()
            coo2 = coo2.todense()

            lst.append([coo0, coo1, coo2])
            len_coo.append(coo0.shape[1])

    except Exception as e:
        print(e)
        break

    nn = min(len_coo)
    coo0 = (lst[0][0][:,:nn] + lst[1][0][:,:nn] + lst[2][0][:,:nn] + lst[3][0][:,:nn])/4
    coo1 = (lst[0][1][:,:nn] + lst[1][1][:,:nn] + lst[2][1][:,:nn] + lst[3][1][:,:nn])/4
    coo2 = (lst[0][2][:,:nn] + lst[1][2][:,:nn] + lst[2][2][:,:nn] + lst[3][2][:,:nn])/4



    fig, (ax1, ax2, ax3) = plt.subplots(3,1, figsize = (10,8))

    # im1 = ax1.imshow(coo0, extent=[0, 1, 0, 1], aspect=10)
    im1 = ax1.imshow(coo0, extent=[0, 20, 0, 8], aspect='auto',
                    interpolation='spline36', cmap=plt.get_cmap('seismic'))
    ax1.set_title(r'$v_r$')
    # ax1.set_xlabel('Radius')
    # ax1.set_ylabel('Length')
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im1.set_clim(vmin=-0.2, vmax=0.2)
    fig.colorbar(im1, cax=cax, orientation='vertical')
    ax1.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax1.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    ax2.set_title(r'$v_{\theta}$')
    # im2 = ax2.imshow(coo1, extent=[0, 1, 0, 1], aspect=10)
    im2 = ax2.imshow(coo1, extent=[0, 20, 0, 8], aspect='auto',
                     interpolation='spline36', cmap=plt.get_cmap('seismic'))
    # ax2.set_xlabel('Radius')
    # ax2.set_ylabel('Length')
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im2.set_clim(vmin=-0.2, vmax=0.2)
    fig.colorbar(im2, cax=cax, orientation='vertical')
    ax2.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax2.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    ax3.set_title(r'$v_z$')
    im3 = ax3.imshow(coo2, extent=[0, 20, 0, 8], aspect='auto',
                     interpolation='spline36', cmap=plt.get_cmap('seismic'))
    # ax3.set_xlabel('Radius')
    # ax3.set_ylabel('Length')
    divider = make_axes_locatable(ax3)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im3.set_clim(vmin=-0.2, vmax=0.2)
    fig.colorbar(im3, cax=cax, orientation='vertical')
    ax3.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax3.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    # plt.show()
    # continue

    if end:
        plt.show()
        break
    if not end:
        plt.savefig(f'sat_v_avg/{trj.snap.time}.png', dpi=100)
        plt.close()


# plt.show()




# run_case(n, iter, skip, max)
