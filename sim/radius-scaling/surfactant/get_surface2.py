import os
import sys 
import numpy as np

from ovito.io import *
from ovito.modifiers import *

grid = 1.2
sc = 2.9

file =  f'pinch_sc{sc}.lammpstrj'
dir = str(sc)

save_dirs = {'profile': f'{dir}/surface_profile2',
             'surf_con': f'{dir}/surface_concentration2',
             'bulk_con': f'{dir}/bulk_concentration2'}

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

# invSel_mod = InvertSelectionModifier()
# delSel_mod = DeleteSelectedModifier()
# pipeline.modifiers.append(invSel_mod)
# pipeline.modifiers.append(delSel_mod)

with open(f'{dir}/breaktime.txt', 'r') as fd:
    breaktime = int(fd.readline())

for i in range(breaktime+10):
    print(i)
    data = pipeline.compute(i)
    surface_positions = data.particles_.positions_[data.particles_.selection != 0]
    positions = data.particles_.positions_
    types = data.particles.particle_types
    
    lz = data.cell.matrix[2,2]
    num_z = round(lz/grid)
    dz = lz/num_z

    sum_x = np.zeros(num_z)
    sum_y = np.zeros(num_z)
    id_count = np.zeros(num_z)
    surf_bins = {}
    for p in surface_positions:
        id = int(np.floor(abs(p[2])/dz))
        if id >= num_z: id-=1 
        sum_x[id] += p[0]
        sum_y[id] += p[1]
        id_count[id] += 1
        xy = [p[0], p[1]]
        surf_bins.setdefault(id, []).append(xy)

    centers = [sum_x/id_count, sum_y/id_count]
    h = np.zeros(num_z)
    for id, coords in surf_bins.items():
        x0 = centers[0][id]
        y0 = centers[1][id]
        n = len(coords)
        for x, y in coords:
            h[id] += np.sqrt((x-x0)**2 + (y-y0)**2)/n

    surf_con = np.zeros(num_z)
    bulk_con = np.zeros(num_z)
    for atom_id, pos in enumerate(positions):
        if types[atom_id] == 3: continue
        id_z = int(np.floor(abs(pos[2])/dz))
        if id_z >= num_z: id_z = num_z-1 
        x0 = centers[0][id_z]
        y0 = centers[1][id_z]
        radius = np.sqrt((pos[0]-x0)**2 + (pos[1]-y0)**2)
        interface = h[id_z]
        # area = 2*np.pi*interface*dz
        # volume = np.pi*interface**2*dz
        thickness = 1.5
        if interface - thickness < radius < interface + thickness:
            surf_con[id_z] += 1
        if radius < interface - thickness:
            bulk_con[id_z] += 1

    with open(f'{save_dirs["profile"]}/{i}.dat', 'w') as fd:
        fd.write((f'# id radius center_X center_Y --dz={dz}\n'))
        for id in range(num_z):
            x0 = centers[0][id]
            y0 = centers[1][id]
            fd.write(f'{id} {h[id]} {x0} {y0}\n')
    
    with open(f'{save_dirs["surf_con"]}/{i}.dat', 'w') as fd:
        fd.write((f'# id con --dz={dz}\n'))
        for id in range(num_z):
            y0 = centers[1][id]
            fd.write(f'{id} {surf_con[id]}\n')

    with open(f'{save_dirs["bulk_con"]}/{i}.dat', 'w') as fd:
        fd.write((f'# id con --dz={dz}\n'))
        for id in range(num_z):
            y0 = centers[1][id]
            fd.write(f'{id} {bulk_con[id]}\n')

