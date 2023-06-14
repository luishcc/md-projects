import os
import sys 
from math import floor
import numpy as np

from mdpkg.rwfile import DumpReader

dz = 1.0
dr = 0.8

file =  'pinch_sc0.5.lammpstrj'
dir = '1'

datafile = '/'.join([dir,file])
save_dir = f'{dir}/surface_profile'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

trj = DumpReader(datafile)
trj.read_sequential()

lz = trj.snap.box.get_length_z()
num_z = round(lz/dz)
dz = lz/num_z

lx = trj.snap.box.get_length_x()
num_r = round(0.5*lx/dr)
dr = lx/num_r

with open(f'{dir}/breaktime.txt', 'r') as fd:
    breaktime = int(fd.readline())

def f_rho(r, R0, D, p_l, p_v=0):
    t1 = 0.5 * (p_l + p_v)
    t2 = 0.5 * (p_l - p_v)
    t3 = np.tanh(2*(r - R0) / D)
    return t1 - t2 * t3

def gibbs_radius(r, rho):
    pl = rho[0]
    pv = 0
    drho = None # compute d/dr(rho)
    integral = [i**2*j*dr for i, j in zip(r,drho)]
    integral = sum(integral)
    return np.sqrt(integral/(pl-pv))
    

for t in range(1, breaktime):
    
    bins = {}
    snap = trj.snap
    for atom in snap.atoms.values():
        idz = floor(abs(atom.position[2]*.999999) / dz)
        bins.setdefault(idz, []).append(atom)

    for bin, atoms in bins.items():

        center = [0,0]
        for atom in atoms:
            center[0] += atom.position[0]
            center[1] += atom.position[1]
        center[0] /= len(atoms)
        center[1] /= len(atoms)

        annuli = {}
        density = {}
        for atom in atoms:
            r = np.sqrt((atom.position[0]-center[0])**2 + (atom.position[1]-center[1])**2)
            idr = floor(r/dr)
            annuli.setdefault(idr, []).append(atom)
            # density.setdefault(idr, 1)





    print()
    print(t)



