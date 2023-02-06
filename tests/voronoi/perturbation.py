import numpy as np
import os

from write import DataFile
from readLammps import DumpReader

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

data = DumpReader('test.dump')

positions = []
for atom in data.atoms:
    positions.append(Point(atom.x))

# atoms_list = Atoms(positions, 1.)

# data = DataFile(box, atoms_list)
# data.write_file('test', os.getcwd())
