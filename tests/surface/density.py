import os
import numpy as np
from math import floor

from mdpkg.rwfile import Dat, CSV, read_dat, DumpReader
from mdpkg.grid import GridSurf

file = 'density2.lammpstrj'


trj = DumpReader(file)
trj.read_sequential()
trj.skip_next(20)
trj.read_next()


num = 100
data = np.zeros((num,4))

lx = trj.snap.box.get_length_x()
ly = trj.snap.box.get_length_y()
lz = trj.snap.box.get_length_z()

sz  = lz/num
vol = lx * ly * sz
ivol = 1/vol

for atom in trj.snap.atoms.values():
    z = atom.position[2] + lz/2
    idz = floor(z/sz)
    print(z, idz)
    type = int(atom.type)
    data[idz][0] += ivol
    data[idz][type] += ivol


import matplotlib.pyplot as plt

z = np.linspace(0,lz,num)

fig, ax = plt.subplots(1,1)

ax.plot(z, data[:,0], 'k-', label='total')
ax.plot(z, data[:,3], 'b-', label='water')
ax.plot(z, data[:,1], 'r-', label='head')
ax.plot(z, data[:,2], 'g-', label='tail')
ax.plot(z, data[:,2]+data[:,1], 'k--', label='surfactant')
ax.legend()

plt.show()
