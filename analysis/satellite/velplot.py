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
dir = '/home/luis/md-projects/sim/satellite'
dir = os.getcwd()


velocity_file = 'dump.vel_14'
trj_file = 'thread_14.lammpstrj'

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
norm = mpl.colors.Normalize(vmin=-0.3, vmax=0.3)

def run2():

    idr = []
    idz = []
    d = [[], [], []]
    dens = []
    force = [[], []]
    for key, cell in grd.cell.items():
        if cell.id[0] >= 8 :
            continue
        idr.append(cell.id[0])
        idz.append(cell.id[2])
        v = cell.get_velocity_cylindrical()
        dens.append(cell.get_density()/cell.nangle)
        d[0].append(v[0]/cell.nangle)
        d[1].append(v[1]/cell.nangle)
        d[2].append(v[2]/cell.nangle)

    idr = [-i + 7 for i in idr]
    coo = coo_matrix((dens, (idr, idz)))
    coo0 = coo_matrix((d[0], (idr, idz)))
    coo1 = coo_matrix((d[1], (idr, idz)))
    coo2 = coo_matrix((d[2], (idr, idz)))
    return coo, coo0, coo1, coo2

trj.skip_next(250)
end = False
while True:
    try:
        trj.read_next()
        trj.read_velocity('/'.join([dir, velocity_file]), trj.snap)
        grd = Grid(trj.snap, size = grid)
        print(trj.snap.time)
        coo, coo0, coo1, coo2 = run2()
    except Exception as e:
        print(e)
        break

    coo = coo.todense()
    coo0 = coo0.todense()
    coo1 = coo1.todense()
    coo2 = coo2.todense()


    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,1, figsize = (10,8))
    # im1 = ax1.imshow(coo0, extent=[0, 1, 0, 1], aspect=10)
    im1 = ax1.imshow(coo0, extent=[0, 20, 0, 4], aspect='auto',
                    interpolation='spline36', cmap=plt.get_cmap('seismic'))
    ax1.set_title(r'$v_r$')
    # ax1.set_xlabel('Radius')
    # ax1.set_ylabel('Length')
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im1.set_clim(vmin=-0.3, vmax=0.3)
    fig.colorbar(im1, cax=cax, orientation='vertical')
    ax1.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax1.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    ax2.set_title(r'$v_{\theta}$')
    # im2 = ax2.imshow(coo1, extent=[0, 1, 0, 1], aspect=10)
    im2 = ax2.imshow(coo1, extent=[0, 20, 0, 4], aspect='auto',
                     interpolation='spline36', cmap=plt.get_cmap('seismic'))
    # ax2.set_xlabel('Radius')
    # ax2.set_ylabel('Length')
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im2.set_clim(vmin=-0.3, vmax=0.3)
    fig.colorbar(im2, cax=cax, orientation='vertical')
    ax2.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax2.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    ax3.set_title(r'$v_z$')
    im3 = ax3.imshow(coo2, extent=[0, 20, 0, 4], aspect='auto',
                     interpolation='spline36', cmap=plt.get_cmap('seismic'))
    # ax3.set_xlabel('Radius')
    # ax3.set_ylabel('Length')
    divider = make_axes_locatable(ax3)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im3.set_clim(vmin=-0.3, vmax=0.3)
    fig.colorbar(im3, cax=cax, orientation='vertical')
    ax3.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax3.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    ax4.set_title('Density')
    im4 = ax4.imshow(coo, extent=[0, 20, 0, 4], aspect='auto',
                     interpolation='spline36')
    # ax4.set_xlabel('Radius')
    # ax4.set_ylabel('Length')
    divider = make_axes_locatable(ax4)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im4.set_clim(vmin=0, vmax=8)
    fig.colorbar(im4, cax=cax, orientation='vertical')
    ax4.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax4.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks

    # plt.show()
    # continue

    if end:
        plt.show()
        break
    if not end:
        plt.savefig(f'sat/{trj.snap.time}.png', dpi=100)
        plt.close()


# plt.show()




# run_case(n, iter, skip, max)

