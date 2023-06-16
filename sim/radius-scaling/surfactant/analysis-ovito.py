import os
import sys 
import numpy as np

from ovito.io import *
from ovito.modifiers import *

grid = 1.2

file =  'pinch_sc0.5.lammpstrj'
dir = '1'

save_dir = f'{dir}/surface_profile'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

pipeline = import_file('/'.join([dir, file]))

surf_mod = ConstructSurfaceModifier(
    method = ConstructSurfaceModifier.Method.AlphaShape,
    radius = 0.8,
    select_surface_particles = True)
pipeline.modifiers.append(surf_mod)

def center_xy(frame, data):
    x = data.particles.positions.T[0]
    y = data.particles.positions.T[1]
    cx = np.sum(x)/len(x)
    cy = np.sum(y)/len(y)
    print(cx,cy, np.sqrt(cx**2+cy**2))
    data.attributes['Center.X'] = cx 
    data.attributes['Center.Y'] = cy

pipeline.modifiers.append(center_xy)

prop_mod = ComputePropertyModifier(
    expressions='sqrt((Position.X-Center.X)^2 + (Position.Y-Center.Y)^2)',
    output_property='Radius2',
    only_selected = True)
pipeline.modifiers.append(prop_mod)

len_z = pipeline.source.data.cell.matrix[2,2]
num_z = round(len_z / grid)
bin_mod = SpatialBinningModifier(
    property = 'Radius2',
    direction = SpatialBinningModifier.Direction.Z,
    bin_count = num_z,
    only_selected = True,
    reduction_operation = SpatialBinningModifier.Operation.Mean)
pipeline.modifiers.append(bin_mod)

data = pipeline.compute()


export_file(pipeline, f'{save_dir}/*.dat', 'txt/table', key='binning', multiple_frames=True)

