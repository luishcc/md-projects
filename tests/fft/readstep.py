import numpy as np
import os


from readLammps import DumpReaderTime
from write import DataFile
from struc import Atoms, Point, Box


filename = 'thread.lammpstrj'

step = 19100

data = DumpReaderTime(filename, step=step)


radius = 6.0
wave_number = 0.55
wave_length = (2 * np.pi * radius) / wave_number

box = Box(6*radius, 6*radius, wave_length)

positions = []
for atom in data.atoms:
    positions.append(Point(atom.x))

atoms_list = Atoms(positions, 1.)

data2 = DataFile(box, atoms_list)
data2.write_file(f'reading_test_{step}', os.getcwd())
