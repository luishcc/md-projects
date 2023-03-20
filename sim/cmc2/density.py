import os
import sys
import numpy as np
from math import floor

from mdpkg.rwfile import Dat, CSV, read_dat, DumpReader
from mdpkg.grid import GridSurf


try:
    sc = sys.argv[1]
    file = '/'.join(['sim', sc, f'sim_{sc}.lammpstrj'])
except IndexError:
    file = 'sim/0.1/sim_0.1.lammpstrj'

trj = DumpReader(file)
trj.read_sequential()
trj.skip_next(10)
trj.read_next()

num = 100
data = np.zeros((num,4))

lx = trj.snap.box.get_length_x()
ly = trj.snap.box.get_length_y()
lz = trj.snap.box.get_length_z()

sz  = lz/num
vol = lx * ly * sz
ivol = 1/vol

area = 2 * lx * ly
iarea = 1/area
con = 0

for atom in trj.snap.atoms.values():
    z = atom.position[2] + lz/2
    idz = floor(z/sz)
#    print(z, idz)
    type = int(atom.type)
    data[idz][0] += ivol
    data[idz][type] += ivol
    if  (z > 43 or z < 27) and type !=3:
        con += iarea

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.7*side, 0.5*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


z = np.linspace(0,lz,num)

fig, ax = plt.subplots(1,1)

z = z-35
ax.plot(z, data[:,0], 'k-', label='total')
ax.plot(z, data[:,3], 'b--', label='water')
ax.plot(z, data[:,1], 'g-.', label='head')
ax.plot(z, data[:,2], 'y-.', label='tail')
ax.plot(z, data[:,2]+data[:,1], 'r--', label='surfactant')
ax.set_xlim(-20, 20)
ax.set_ylim(0, 6.3)
ax.set_ylabel(r'$\rho$ $[N/V]$')
ax.set_xlabel(r'$z$')
ax.text(-18,5, fr'$\phi = {round(con/4,2)}$')
ax.legend(frameon=False)

plt.tight_layout()
plt.savefig(f'dense-{sc}.pdf', dpi=dpi)
plt.show()
