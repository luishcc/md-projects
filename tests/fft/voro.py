import numpy as np
import os

from readLammps import DumpReader
from write import DataFile

from struc import Atoms, Point, Box

from readLammps import Voronoi as voro_read

from scipy.spatial import Voronoi

import matplotlib.pyplot as plt


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
    plt.xlim(0,30)

    plt.subplot(133)
    mu = stats.tmean(v, (0.1,0.2))
    sigma = stats.tstd(v, (0.1,0.2))
    x = np.linspace(mu - 5*sigma, mu + 5*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma))
    plt.xlim(0,0.3)
    plt.show()


def plot_volume_distribution2(v):
    import scipy.stats as stats
    #import seaborn as sns

    #sns.set(color_codes=True)
    #sns.set(rc={'figure.figsize':(5,5)})
    fig, ax = plt.subplots(1, 1)

    dat = stats.gamma.fit(v)
    #ax = sns.distplot(dat,
                  # kde=True,
                  # bins=100,
                  # color='skyblue',
                  # hist_kws={"linewidth": 15,'alpha':1})
    ax.hist(v,density=True, histtype='bar', alpha=0.3, bins =10000)
    ax.set_xlim(0,4)
    plt.show()


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi

def readVor(file_name):
    pos = []
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
            pos.append(coo)
            vol.append(float(l[5]))
            if float(l[5]) > .3:
                surf.append(coo)
    return pos, surf, vol


pos, surf, volumes = readVor('dump.voro')

plot_volume_distribution(volumes)
exit()

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
