import os
import sys
# import numpy as np

from mdpkg.rwfile import Dat, CSV, read_dat, DumpReader
from mdpkg.grid import GridSurf

sc = 2.6
time_file = f'/home/luishcc/hdd/surfactant/R8-{sc}/1/breaktime.txt'
trj_file = f'/home/luishcc/hdd/surfactant/R8-{sc}/1/cylinder_8_{sc}.lammpstrj'

with open(time_file, 'r') as fd:
    snap = int(fd.readline())

thickness = 2

snap = 1

surf_file = f'sc-{sc}-{snap}.dat'
#
trj = DumpReader(trj_file)
# print('Mapping snapshots in file')
# trj.map_snapshot_in_file2()
# trj.start_read()
# print('Reading snapshot')
# trj.read_snapshot_at2((snap+1)*1000)

trj.read_sequential()
trj.skip_next(snap-1)


print('Reading Shape')
z = []
dense = []
dense2 = []
shape = []
with open(surf_file, 'r') as fd:
    fd.readline()
    fd.readline()
    for line in fd:
        line = line.split(' ')
        z.append(float(line[0]))
        dense.append(0)
        dense2.append(0)
        shape.append(float(line[1]))

print('Making Grid')
grd = GridSurf(trj.snap, shape=shape, thickness=thickness)
grd = GridSurf(trj.snap, shape=[1.2]*len(shape), thickness=1.2)

print("Run and plot")
for idz, cell in grd.cell.items():
    # foo = cell.get_area_density_type
    foo = cell.get_density_type
    dense[idz] = foo(1)+foo(2)
    dense2[idz] = foo(3)

AA = 0
for idz, cell in grd.cell.items():
    AA += cell.area

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import container
dpi = 1600
side = 5
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (1.8*side, 1.0*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


fig, (ax,ax2) = plt.subplots(2,1, sharex = True)

# ax.plot(z, [i/4 for i in dense], 'r-', label='Surfactant')
# ax.plot(z[:], dense2[:], 'b-', label='Water')
# ax.plot(z,[i+j for i,j in zip(dense,dense2)], 'r-', label='TT')
ax.plot(z,[i/(j+i) for i,j in zip(dense,dense2)], 'r-', label='Surfactant')
# ax.plot(z, [0.5250118552398716]*len(z), 'r-', label='sc')
# ax.plot(z, [0.6024108744138862]*len(z), 'r-')
# ax.plot(z, [1.2599730481179077]*len(z), 'r-')
# ax.plot(z[:],[j/(j+i) for i,j in zip(dense[:],dense2[:])], 'b-', label='wc')
ax.set_ylabel(r'$N_s/N$')
# ax.set_ylabel(r'$N_s/A$')
ax.set_xlabel(r'$z$')
ax.legend(frameon=False)
# ax.set_ylim(0.7, 1.8)

ax2.plot(z, shape, 'k-', label='Surface profile')
ax2.plot(z, [i-thickness*.9 for i in shape], 'k--', label='Thickness')
ax2.plot(z, [i+thickness*.1 for i in shape], 'k--')



ax2.plot(z, [-i for i in shape], 'k-')
ax2.plot(z, [-i+thickness*.9 for i in shape], 'k--')
ax2.plot(z, [-i-thickness*.1 for i in shape], 'k--')

ax2.plot(z, [0]*len(z), 'k-.')
ax2.set_ylim(-60,60)
ax2.set_ylabel(r'$r$')
ax2.set_xlabel(r'$z$')
ax2.legend(frameon=False)


plt.tight_layout()
plt.savefig(f'{snap}.pdf', dpi=dpi)

plt.show()
