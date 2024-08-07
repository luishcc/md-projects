import os
import numpy as np
import math
import PySide6.QtWidgets

app = PySide6.QtWidgets.QApplication()
os.environ['OVITO_GUI_MODE'] = '1'

import ovito
from ovito.io import *
from ovito.vis import *
from ovito.modifiers import *

# from mdpkg.rwfile import Dat, CSV, read_dat, DumpReader
# from mdpkg.grid import Gridz


grid = 1.2
frame = 20

file = 'testA853.lammpstrj'


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


# data = pipeline.compute(frame)
data = pipeline.compute()
# pipeline.add_to_scene()
# data.particles.vis.radius = 0.3

export_file(pipeline, f'files7/sc-*.dat', 'txt/table', key='binning', multiple_frames=True)

# vp.zoom_all((800,600))
# vp.render_image(
#     size=(800,600),
#     filename='test.png',
#     background=(1,1,1),
#     frame=frame)
