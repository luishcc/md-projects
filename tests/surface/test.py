from ovito.io import *
from ovito.modifiers import *

from scipy.linalg import eig, inv
import numpy as np

from mdpkg.rwfile import Dat, CSV, read_dat

import os

grid = 0.7

file = 'test.lammpstrj'

pipeline = import_file(file)
surf_mod = ConstructSurfaceModifier(
    method = ConstructSurfaceModifier.Method.AlphaShape,
    radius = 0.8,
    select_surface_particles = True)
pipeline.modifiers.append(surf_mod)

# pipeline.modifiers.append(InvertSelectionModifier())
# pipeline.modifiers.append(DeleteSelectedModifier())

prop_mod = ComputePropertyModifier(
    expressions='sqrt(Position.X^2 + Position.Y^2)',
    output_property='Radius',
    only_selected = True)
pipeline.modifiers.append(prop_mod)

len_z = pipeline.source.data.cell.matrix[2,2]
num_z = round(len_z / grid)
bin_mod = SpatialBinningModifier(
    property = 'Radius',
    direction = SpatialBinningModifier.Direction.Z,
    bin_count = num_z,
    only_selected = True,
    reduction_operation = SpatialBinningModifier.Operation.Mean)
pipeline.modifiers.append(bin_mod)

# export_file(pipeline, 'output/density.vtk', 'vtk/grid', key='binning')

data = pipeline.compute(295)
