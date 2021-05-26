import numpy as np
import os

from readLammps import DumpReader
from write import DataFile

from readLammps import Voronoi as voro_read

from scipy.spatial import Voronoi

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib as mpl


def readVor(file_name):
    pos = []
    surf = []
    file = open(file_name, 'r')
    reading_entry = False

    for line in file:

        if line.find('ITEM: ATOMS') >= 0:
            reading_entry = True
            continue

        if reading_entry:
            l = line.split()
            coo = [float(l[2]), float(l[3]), float(l[4])]
            pos.append(coo)
            if float(l[5]) > .3:
                surf.append(coo)
    return pos, surf

data = DumpReader('test.dump')


p2 = np.array([[0, 0], [0, 0.5], [0, 1],
               [0.5, 0.25], [0.5, 0.75],
               [1, 0], [1, 0.5], [1, 1]])


points = np.zeros((len(data.atoms), 3))

for atom in data.atoms:
    points[atom.id, 0] = atom.x[0]
    points[atom.id, 1] = atom.x[1]
    points[atom.id, 2] = atom.x[2]

vor = Voronoi(points)
vor2 = Voronoi(p2)

vor3 = voro_read('dump.neighbors')


pos, surf = readVor('dump.voro')

px = [sub[0] for sub in pos]
py = [sub[1] for sub in pos]
pz = [sub[2] for sub in pos]

sx = [sub[0] for sub in surf]
sy = [sub[1] for sub in surf]
sz = [sub[2] for sub in surf]


class Point:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

class Atoms:
    def __init__(self, points, density):
        self.number = len(points)
        self.positions = points
        self.density = density
        return

class Box:
    def __init__(self, lx, ly, lz):
        self.xlo = -lx/2.
        self.xhi = lx/2.
        self.ylo = -ly/2.
        self.yhi = ly/2.
        self.zlo = 0
        self.zhi = lz


radius = 6.0
wave_number = 0.6
wave_length = (2 * np.pi * radius) / wave_number

box = Box(6*radius, 6*radius, wave_length)

positions = []
for i in range(len(sx)):
    positions.append(Point([sx[i],sy[i],sz[i]]))

atoms_list = Atoms(positions, 1.)

print('111')
data = DataFile(box, atoms_list)
print('222')
data.write_file('surf', os.getcwd())
print('333')

exit()
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.grid(False)
plt.axis('off')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
#ax.plot(px, py, pz, 'k.')
ax.plot(sx, sy, sz, 'b.')
plt.show()
