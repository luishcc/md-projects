import numpy as np
import os

from readLammps import DumpReader
from write import DataFile

from perturbation import Point, Box

from readLammps import Voronoi as voro_read

from scipy.spatial import Voronoi

import matplotlib.pyplot as plt

class Atoms2:
    def __init__(self, points, density, types):
        self.number = len(points)
        self.positions = points
        self.density = density
        self.types = types
        return

def plot_volume_distribution(v):
    import scipy.stats as stats

    mu = stats.tmean(v)
    sigma = stats.tstd(v)
    x = np.linspace(mu - 5*sigma, mu + 5*sigma, 100)

    plt.figure(1)
    plt.subplot(131)
    plt.plot(np.linspace(0, max(v), len(v)), v, 'k.')

    plt.subplot(132)
    plt.plot(x, stats.norm.pdf(x, mu, sigma))
    plt.xlim(0,150)

    plt.subplot(133)
    mu = stats.tmean(v, (0.05,0.3))
    sigma = stats.tstd(v, (0.05,0.3))
    x = np.linspace(mu - 5*sigma, mu + 5*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma))
    plt.xlim(0,0.3)
    plt.show()



def readVor(file_name):
    pos = []
    types = []
    surf = []
    vol = []
    file = open(file_name, 'r')
    reading_entry = False

    for line in file:

        if line.find('ITEM: ATOMS') >= 0:
            reading_entry = True
            continue

        if reading_entry:
            l = line.split()
            coo = [float(l[2]), float(l[3]), float(l[4])]
            type = int(l[1])
            pos.append(coo)
            vol.append(float(l[5]))
            if float(l[5]) > .23:
                surf.append(coo)
                types.append(type)

    return pos, surf, vol, types

# data = DumpReader('test.dump')


p2 = np.array([[0, 0], [0, 0.5], [0, 1],
               [0.5, 0.25], [0.5, 0.75],
               [1, 0], [1, 0.5], [1, 1]])


# points = np.zeros((len(data.atoms), 3))

# for atom in data.atoms:
#     points[atom.id, 0] = atom.x[0]
#     points[atom.id, 1] = atom.x[1]
#     points[atom.id, 2] = atom.x[2]

#vor = Voronoi(points)
#vor2 = Voronoi(p2)

#vor3 = voro_read('dump.neighbors')


pos, surf, volumes, types = readVor('dump.voronoi')

# plot_volume_distribution(volumes)
# exit()

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


atoms_list1 = Atoms2(positions, 1., types)
# print(types, type(types))

data = DataFile(box, atoms_list1)
data.write_file('surf-5', os.getcwd())

# box = Box((max(sr)-min(sr))*2, 2*np.pi*radius, wave_length)
#
# positions = []
# for i in range(len(sx)):
#     positions.append(Point([ sr[i]-radius, st[i]*radius, sz[i] ]))
#
# atoms_list = Atoms(positions, types)
# print(types)
#
# data = DataFile(box, atoms_list)
# data.write_file('surf-pol', os.getcwd())
