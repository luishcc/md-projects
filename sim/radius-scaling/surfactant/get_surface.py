import os
import sys 
import numpy as np

from ovito.io import *
from ovito.modifiers import *

grid = 1.2

file = sys.argv[2]
dir = sys.argv[1]

save_dir = f'{dir}/surface_profile'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

pipeline = import_file('/'.join([dir, file]))
surf_mod = ConstructSurfaceModifier(
    method = ConstructSurfaceModifier.Method.AlphaShape,
    radius = 0.8,
    select_surface_particles = True)
pipeline.modifiers.append(surf_mod)

prop_mod = ComputePropertyModifier(
    expressions='sqrt(Position.X^2 + Position.Y^2)',
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

