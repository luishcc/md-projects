import os
import sys

import ovito
from ovito.io import *
from ovito.modifiers import *


try:
    sc = sys.argv[1]
except IndexError:
    sc = 0.5

file = f'{sc}/sim_{sc}.lammpstrj'

pipeline = import_file(file)

select_mod = ExpressionSelectionModifier(
    expression = '(Position.Z > 8 || Position.Z < -8) && ParticleType != 3')
pipeline.modifiers.append(select_mod)


lx = pipeline.source.data.cell.matrix[0,0]
ly = pipeline.source.data.cell.matrix[1,1]

timeAvg_mod =TimeAveragingModifier(
    operate_on='attribute:ExpressionSelection.count',
    interval = (10,pipeline.source.num_frames))
pipeline.modifiers.append(timeAvg_mod)

data = pipeline.compute()

con = data.attributes['ExpressionSelection.count (Average)']/(4*2*lx*ly)

print(con)
with open(f'{sc}/sc.dat', 'w') as fd:
    fd.write(str(con))
