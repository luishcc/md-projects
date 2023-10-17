import os
import sys
import numpy as np
from math import floor

from mdpkg.rwfile import Dat, CSV, read_dat, DumpReader
from mdpkg.grid import GridSurf


try:
    sc = sys.argv[1]
    file = '/'.join(['sim', sc, f'sim_{sc}.lammpstrj'])
except Exception as e:
    print(e)
    sc = '0.1'
    file = 'sim/0.1/sim_0.1.lammpstrj'

trj = DumpReader(file)
trj.read_sequential()
trj.skip_next(10)
trj.read_next()

num = 200
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

count=0
while True:
    print(count)
    for atom in trj.snap.atoms.values():
        z = atom.position[2] + lz/2
        idz = floor(z/sz)
        type = int(atom.type)
        if idz >= num:
            data[num-1][0] += ivol
            data[num-1][type] += ivol
            continue
        elif idz < 0:
            data[0][0] += ivol
            data[0][type] += ivol
            continue
        data[idz][0] += ivol
        data[idz][type] += ivol        
        if  (z > 43 or z < 27) and type !=3:
            con += iarea
    count += 1
    try:
        trj.read_next()
    except Exception as e:
        print(e)
        break

data = data/count

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.5*side, 0.4*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


z = np.linspace(-lz/2,lz/2,num)

fig, ax = plt.subplots(1,1)

# z = z-35
# ax.plot(z, data[:,0], 'k-', label='total')
ax.plot(z, data[:,3], 'b-', label='W', markerfacecolor='none')
ax.plot(z, data[:,1], 'r-.', label='H', markerfacecolor='none')
ax.plot(z, data[:,2], 'y--', label='T', markerfacecolor='none')
# ax.plot(z, data[:,2]+data[:,1], 'r--', label='surfactant')
# ax.set_xlim(-20, 20)
ax.set_xlim(0, 15)
ax.set_ylim(0, 6.3)
ax.set_ylabel(r'$\rho$ $[N/V]$')
ax.set_xlabel(r'$z$ [$r_c$]')
# ax.text(-18,5, fr'$\phi = {round(con/4,2)}$')
ax.legend(frameon=False, loc='center left')

plt.tight_layout()
plt.savefig(f'dense-{sc}.pdf', dpi=dpi)
plt.show()
