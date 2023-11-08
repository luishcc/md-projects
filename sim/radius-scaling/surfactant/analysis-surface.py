import os
import sys 
from math import floor
import numpy as np
from scipy.optimize import curve_fit

from mdpkg.rwfile import DumpReader

file =  'pinch_sc0.5.lammpstrj'
dir = '0.5'

datafile = '/'.join([dir,file])
save_dir = f'{dir}/surface_concentration'

with open(f'{dir}/breaktime.txt', 'r') as fd:
    breaktime = int(fd.readline())

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

trj = DumpReader(datafile)
trj.read_sequential()
trj.skip_next(50)
trj.read_next()


dz = 1.2
surface_thickness = 1.5

lz = trj.snap.box.get_length_z()
num_z = round(lz/dz)
dz = lz/num_z
z = np.linspace(0, lz, num_z)

centers = {}
with open(f'{dir}/surface_profile/center.dat', 'r') as fd:
    fd.readline()
    for line in fd:
        line = line.split(' ')
        centers[int(line[0])] = [float(line[1]), float(line[2])]

def get_surface(time):
    time_id = int((time - min(centers.keys())) * .01)
    z = []
    h = []
    with open(f'{dir}/surface_profile/{time_id}.dat', 'r' ) as fd:
        fd.readline()
        fd.readline()
        for line in fd:
            line = line.split(' ')
            z.append(float(line[0]))
            h.append(float(line[1]))
    return z, h
              

def run_snapshot(snapshot):  

    bins = {}
    n_bulk = {}
    n_surface = {}
    surface_z, surface_h = get_surface(snap.time)
    center = centers[snap.time]

    for atom in snapshot.atoms.values():

        idz = floor(abs(atom.position[2]) / dz)
        bins.setdefault(idz, []).append(atom)

        r = np.sqrt((atom.position[0]-center[0])**2 + (atom.position[1]-center[1])**2)
        thickness_plus = surface_h[idz] + 0.25*surface_thickness
        thickness_minus = surface_h[idz] - 0.85*surface_thickness 
        key = (idz, atom.type)
        if thickness_minus < r < thickness_plus:
            n_surface[key] = n_surface.setdefault(key, 0) + 1
        elif r <= thickness_minus:
            n_bulk[key] = n_bulk.setdefault(key, 0) + 1

    return n_bulk, n_surface, bins


def run_avg(num):
    pass


