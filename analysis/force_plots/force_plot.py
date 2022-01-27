import sys
import os
from math import floor, ceil

import numpy as np
from scipy.sparse import coo_matrix

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica"
})


from mdpkg.rwfile import DumpReader, Dat
from mdpkg.grid import Grid


dir = '/home/luishcc/testdata'
dir = '/home/luishcc/md-projects/tests/rerun'

force_file = 'force.test'
trj_file = 'test.lammpstrj'

force_file = 'dump.force2'
velocity_file = 'dump.vel2'
trj_file = 'thread2.lammpstrj'

force_file = 'dump.force'
velocity_file = 'dump.vel'
trj_file = 'thread.lammpstrj'



# force_file = 'dump.force2'
# trj_file = 'thread2.lammpstrj'

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
norm = mpl.colors.Normalize(vmin=-10, vmax=10)

def run2():

    idr = []
    idz = []
    d = [[], [], []]
    dens = []
    force = [[], []]
    for key, cell in grd.cell.items():
        if cell.id[0] >= 4 :
            continue
        idr.append(cell.id[0])
        idz.append(cell.id[2])
        force = cell.get_force_cylindrical()
        dens.append(cell.get_density()/cell.nangle)
        d[0].append(force[0]/cell.nangle)
        d[1].append(force[1]/cell.nangle)
        d[2].append(force[2]/cell.nangle)

    idr = [-i+3 for i in idr]
    coo = coo_matrix((dens, (idr, idz)))
    coo0 = coo_matrix((d[0], (idr, idz)))
    coo1 = coo_matrix((d[1], (idr, idz)))
    coo2 = coo_matrix((d[2], (idr, idz)))
    return coo, coo0, coo1, coo2

trj.skip_next(0)
end = False
while True:
    try:
        trj.read_next()
        trj.read_force('/'.join([dir, force_file]), trj.snap)
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

    im1 = ax1.imshow(coo0, extent=[0, 20, 0, 4], aspect='auto',
                    interpolation='spline36', cmap=plt.get_cmap('seismic'))
    ax1.set_title(r'$F_r$')
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im1.set_clim(vmin=-20, vmax=20)
    fig.colorbar(im1, cax=cax, orientation='vertical')
    ax1.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax1.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    ax2.set_title(r'$F_{\theta}$')
    im2 = ax2.imshow(coo1, extent=[0, 20, 0, 4], aspect='auto',
                     interpolation='spline36', cmap=plt.get_cmap('seismic'))
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im2.set_clim(vmin=-15, vmax=15)
    fig.colorbar(im2, cax=cax, orientation='vertical')
    ax2.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
    ax2.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


    ax3.set_title(r'$F_z$')
    im3 = ax3.imshow(coo2, extent=[0, 20, 0, 4], aspect='auto',
                     interpolation='spline36', cmap=plt.get_cmap('seismic'))
    divider = make_axes_locatable(ax3)
    cax = divider.append_axes('right', size='3%', pad=0.2)
    im3.set_clim(vmin=-15, vmax=15)
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
        plt.savefig(f'small-f/{trj.snap.time}.png', dpi=100)
        plt.close()


# plt.show()




# run_case(n, iter, skip, max)
