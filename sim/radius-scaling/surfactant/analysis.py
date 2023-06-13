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

# TO DO get breaktime snap
for t in range(1, breaktime):
    
    bins = {}
    snap = trj.snap
    for atom in snap.atoms.values():
        idz = floor(atom.position[2]*.999999 / dz)
        bins.setdefault(idz, []).append(atom)

    for bin in bins.values():
        pass


