import os
import sys 
import numpy as np

from ovito.io import *
from ovito.modifiers import *

grid = 1.2
sc = 80

file =  f'pinch_A{sc}.lammpstrj'
dir = '/home/luishcc/hdd/radius_scaling/high-Oh/1'

save_dirs = {'profile': f'{dir}/surface_profile'}

for sdir in save_dirs.values():
    if not os.path.exists(sdir):
        os.makedirs(sdir)

pipeline = import_file('/'.join([dir, file]))

# Create surface and select particles on the surface
surf_mod = ConstructSurfaceModifier(
    method = ConstructSurfaceModifier.Method.AlphaShape,
    radius = 0.8,
    select_surface_particles = True)
pipeline.modifiers.append(surf_mod)

with open(f'{dir}/breaktime.txt', 'r') as fd:
    breaktime = int(fd.readline())

for frame in range(pipeline.source.num_frames):
    print(frame)
    data = pipeline.compute(frame)
  
    surface_positions = data.particles_.positions_[data.particles_.selection != 0]
    positions = data.particles_.positions_
    
    lz = data.cell.matrix[2,2]
    num_z = round(lz/grid)
    dz = lz/num_z

    sum_x = np.zeros(num_z, dtype='int32')
    sum_y = np.zeros(num_z, dtype='int32')
    id_count = np.zeros(num_z, dtype='int32')
    surf_bins = {}
    for p in surface_positions:
        id = int(np.floor(abs(p[2])/dz))
        if id >= num_z: id-=1 
        sum_x[id] += p[0]
        sum_y[id] += p[1]
        id_count[id] += 1
        xy = [p[0], p[1]]
        surf_bins.setdefault(id, []).append(xy)

    if not id_count.all() : break
    centers = [sum_x/id_count, sum_y/id_count]

    h = np.zeros(num_z)
    for id, coords in surf_bins.items():
        x0 = centers[0][id]
        y0 = centers[1][id]
        n = len(coords)
        for x, y in coords:
            h[id] += np.sqrt((x-x0)**2 + (y-y0)**2)/n

    with open(f'{save_dirs["profile"]}/{frame}.dat', 'w') as fd:
        fd.write((f'# id radius center_X center_Y --dz={dz} --N={num_z}\n'))
        for id in range(num_z):
            x0 = centers[0][id]
            y0 = centers[1][id]
            fd.write(f'{id} {h[id]} {x0} {y0}\n')

with open(f'{dir}/breaktime.txt', 'w') as fd:
    fd.write((f'{frame}'))
    