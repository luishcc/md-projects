import os
import sys
from math import floor
import numpy as np
from mdpkg.rwfile import DumpReader, Dat

#############################################################
# Some directories and analysis properties definitions

try:
    sc = sys.argv[1]
except:
    sc = '2.3'

concentration = sc.split('/')[0]

file =  f'pinch_sc{concentration}.lammpstrj'
dir = sc


print(dir)

if concentration == '0.5':
    surface_thickness = 1
elif concentration == '1.6':
    surface_thickness = 1.7
else:
    surface_thickness = 2

dz = 1.2

datafile = '/'.join([dir,file])
save_dir_surf = f'{dir}/surface_concentration'
save_dir_bulk = f'{dir}/bulk_concentration'
if not os.path.exists(save_dir_bulk):
    os.makedirs(save_dir_bulk)
if not os.path.exists(save_dir_surf):
    os.makedirs(save_dir_surf)

with open(f'{dir}/breaktime.txt', 'r') as fd:
    breaktime = int(fd.readline())

trj = DumpReader(datafile)
trj.read_sequential()
trj.skip_next(300)
trj.read_next()

lz = trj.snap.box.get_length_z()
num_z = round(lz/dz)
dz = lz/num_z
z = np.linspace(0, lz, num_z)

# Nothing important in the analysis until this point
#############################################################


#############################################################
# The cylinder can move sometimes in the xy plane,
# Centers is a dict that stores the cylinder's center position
#
# centers[<timestep>] = [X, Y]
#
# OBS: center.dat file stores simulation timestep value and not 
# the snapshot number
 
centers = {}
with open(f'{dir}/surface_profile/center.dat', 'r') as fd:
    fd.readline()
    for line in fd:
        line = line.split(' ')
        centers[int(line[0])] = [float(line[1]), float(line[2])]
# print(centers)

#############################################################

# Code working until this point, 
# possible sources of error in results:
# - Computing the cylinder's center with ovito (center.dat)
# - Not tracking center of each bin separetly

#############################################################

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
    # bins = {}
    n_bulk = {}
    n_surface = {}
    surface_z, surface_h = get_surface(snapshot.time)
    center = centers[snapshot.time]
    for atom in snapshot.atoms.values():
        idz = floor(abs(atom.position[2]) / dz)
        if idz > len(surface_h)-1:
            idz = len(surface_h)-1
        # bins.setdefault(idz, []).append(atom)
        r = np.sqrt((atom.position[0]-center[0])**2 + (atom.position[1]-center[1])**2)
        thickness_plus = surface_h[idz] + surface_thickness
        thickness_minus = surface_h[idz] - surface_thickness 
        key = (idz, atom.type)
        if max(thickness_minus,0) < r < thickness_plus:
            n_surface[key] = n_surface.setdefault(key, 0) + 1
        elif r <= thickness_minus:
            n_bulk[key] = n_bulk.setdefault(key, 0) + 1
    return n_bulk, n_surface

def run_avg(num):
    nb_avg = {}
    ns_avg = {}
    for i in range(num):
        snapshot = trj.snap
        nb, ns = run_snapshot(snapshot)
        for key in ns.keys() | nb.keys():
            nb_avg[key] = nb_avg.setdefault(key, 0) + nb.setdefault(key, 0)/num
            ns_avg[key] = ns_avg.setdefault(key, 0) + ns.setdefault(key, 0)/num
        trj.read_next()
    return nb_avg, ns_avg

num_avg = 4
for i in range(breaktime//num_avg-1):
    time = trj.snap.time
    id_t = int((time - min(centers.keys())) * .01)
    print(id_t)
    nb, ns = run_avg(num_avg)
    surf_file = open(f'{save_dir_surf}/{id_t}.dat', 'w')
    surf_file.write('# id type N\n')
    bulk_file = open(f'{save_dir_bulk}/{id_t}.dat', 'w')
    bulk_file.write('# id type N\n')
    for key in sorted(ns.keys()):
        id, type = key
        surf_file.write(f'{id} {type} {ns[key]}\n')
        bulk_file.write(f'{id} {type} {nb[key]}\n')
    surf_file.close()
    bulk_file.close()




