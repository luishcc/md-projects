import os
import sys
# import numpy as np

from mdpkg.rwfile import Dat, CSV, read_dat, DumpReader
from mdpkg.grid import GridSurf

file = 'test.lammpstrj'
try:
    frame = int(sys.argv[1])
except IndexError:
    frame = 20

thickness = 3

surf_file = f'sc-{frame}.dat'
#
trj = DumpReader(file)
trj.map_snapshot_in_file2()
trj.start_read()
trj.read_snapshot_at2((frame+1)*1000)

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


grd = GridSurf(trj.snap, shape=shape, thickness=thickness)


for idz, cell in grd.cell.items():
    foo = cell.get_area_density_type
    # foo = cell.get_density_type
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

ax.plot(z[:], [i/4 for i in dense[:]], 'k-', label='Surfactant')
# ax.plot(z[:-2], dense2[:-2], 'b-', label='Water')
ax.set_ylabel(r'$\phi_s$')
ax.set_xlabel(r'$z$')
ax.legend(frameon=False)
ax.set_ylim(0.7, 1.8)

ax2.plot(z, shape, 'k-', label='Surface profile')
ax2.plot(z, [i-thickness*.9 for i in shape], 'k--', label='Thickness')
ax2.plot(z, [i+thickness*.1 for i in shape], 'k--')
ax2.set_ylim(0,15)
ax2.set_ylabel(r'$r$')
ax2.set_xlabel(r'$z$')
ax2.legend(frameon=False)


plt.tight_layout()
plt.savefig(f'{frame}.pdf', dpi=dpi)

plt.show()
