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

force_file = 'dump.force'
trj_file = 'threads.lammpstrj'

grid = 2

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

trj.skip_next(170)
trj.read_next()
trj.read_force('/'.join([dir, force_file]), trj.snap)
grd = Grid(trj.snap, size = grid)
print(trj.snap.time)


idr = []
idz = []
d = [[], [], []]
dens = []
for key, cell in grd.cell.items():
    idr.append(cell.id[0])
    idz.append(cell.id[2])
    force = cell.get_force_cylindrical()
    dens.append(cell.get_density()/cell.nangle)
    d[0].append(force[0]/cell.nangle)
    d[1].append(force[1]/cell.nangle)
    d[2].append(force[2]/cell.nangle)


from scipy.sparse import coo_matrix
coo = coo_matrix((dens, (idr, idz)))
coo0 = coo_matrix((d[0], (idr, idz)))
coo1 = coo_matrix((d[1], (idr, idz)))
coo2 = coo_matrix((d[2], (idr, idz)))

trj.read_next()
trj.read_force('/'.join([dir, force_file]), trj.snap)
grd = Grid(trj.snap, size = grid)
print(trj.snap.time)

idr = []
idz = []
d = [[], [], []]
dens = []
for key, cell in grd.cell.items():
    idr.append(cell.id[0])
    idz.append(cell.id[2])
    force = cell.get_force_cylindrical()
    dens.append(cell.get_density()/cell.nangle)
    d[0].append(force[0]/cell.nangle)
    d[1].append(force[1]/cell.nangle)
    d[2].append(force[2]/cell.nangle)

coo += coo_matrix((dens, (idr, idz)))
coo0 += coo_matrix((d[0], (idr, idz)))
coo1 += coo_matrix((d[1], (idr, idz)))
coo2 += coo_matrix((d[2], (idr, idz)))

trj.read_next()
trj.read_force('/'.join([dir, force_file]), trj.snap)
grd = Grid(trj.snap, size = grid)
print(trj.snap.time)

idr = []
idz = []
d = [[], [], []]
dens = []
for key, cell in grd.cell.items():
    idr.append(cell.id[0])
    idz.append(cell.id[2])
    force = cell.get_force_cylindrical()
    dens.append(cell.get_density()/cell.nangle)
    d[0].append(force[0]/cell.nangle)
    d[1].append(force[1]/cell.nangle)
    d[2].append(force[2]/cell.nangle)

coo += coo_matrix((dens, (idr, idz)))
coo0 += coo_matrix((d[0], (idr, idz)))
coo1 += coo_matrix((d[1], (idr, idz)))
coo2 += coo_matrix((d[2], (idr, idz)))


coo = coo.todense().transpose()/3
coo0 = coo0.todense().transpose()/3
coo1 = coo1.todense().transpose()/3
coo2 = coo2.todense().transpose()/3

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1,4)
# im1 = ax1.imshow(coo0, extent=[0, 1, 0, 1], aspect=10)
im1 = ax1.imshow(coo0)
ax1.set_title(r'F_r')
ax1.set_xlabel('Radius')
ax1.set_ylabel('Length')
divider = make_axes_locatable(ax1)
cax = divider.append_axes('right', size='50%', pad=0.1)
fig.colorbar(im1, cax=cax, orientation='vertical')
ax1.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
ax1.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks


# fig, ax = plt.subplots(1,1)
ax2.set_title('F_t')
# im2 = ax2.imshow(coo1, extent=[0, 1, 0, 1], aspect=10)
im2 = ax2.imshow(coo1)
ax2.set_xlabel('Radius')
ax2.set_ylabel('Length')
divider = make_axes_locatable(ax2)
cax = divider.append_axes('right', size='50%', pad=0.1)
fig.colorbar(im2, cax=cax, orientation='vertical')
ax2.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
ax2.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks
# fig.set_dpi(460)


# fig, ax = plt.subplots(1,1)
ax3.set_title('F_z')
# im3 = ax3.imshow(coo2, extent=[0, 1, 0, 1], aspect=10)
im3 = ax3.imshow(coo2)
ax3.set_xlabel('Radius')
ax3.set_ylabel('Length')
divider = make_axes_locatable(ax3)
cax = divider.append_axes('right', size='50%', pad=0.1)
fig.colorbar(im3, cax=cax, orientation='vertical')
ax3.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
ax3.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks
# fig.set_dpi(460)


# fig, ax = plt.subplots(1,1)
ax4.set_title('Density')
# im4 = ax4.imshow(coo, extent=[0, 1, 0, 1], aspect=10)
im4 = ax4.imshow(coo)
ax4.set_xlabel('Radius')
ax4.set_ylabel('Length')
divider = make_axes_locatable(ax4)
cax = divider.append_axes('right', size='50%', pad=0.1)
fig.colorbar(im4, cax=cax, orientation='vertical')
ax4.yaxis.set_major_locator(plt.NullLocator()) # remove y axis ticks
ax4.xaxis.set_major_locator(plt.NullLocator()) # remove x axis ticks
# fig.set_dpi(460)

plt.show()




# run_case(n, iter, skip, max)
