import numpy as np
import os

from readLammps import DumpReader
from write import DataFile

from perturbation import Atoms, Point, Box

from readLammps import Voronoi as voro_read

from scipy.spatial import Voronoi

import matplotlib.pyplot as plt



def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi

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

sr = np.zeros(len(sx))
st = np.zeros(len(sx))
for i in range(len(sx)):
    sr[i], st[i] = cart2pol(sx[i], sy[i])

radius = 6.0
wave_number = 0.6
wave_length = (2 * np.pi * radius) / wave_number

box = Box(6*radius, 6*radius, wave_length)

positions = []
for i in range(len(sx)):
    positions.append(Point([sx[i],sy[i],sz[i]]))

atoms_list = Atoms(positions, 1.)

data = DataFile(box, atoms_list)
data.write_file('surf', os.getcwd())


box = Box((max(sr)-min(sr))*2, 2*np.pi*radius, wave_length)

positions = []
for i in range(len(sx)):
    positions.append(Point([ sr[i]-radius, st[i]*radius, sz[i] ]))

atoms_list = Atoms(positions, 1.)

data = DataFile(box, atoms_list)
data.write_file('surf-pol', os.getcwd())
