import os
import sys

import numpy as np
from scipy.interpolate import CubicSpline

from ovito.io import *
from ovito.modifiers import *

dir = sys.argv[1]
print(dir)

if os.path.isfile(f'{dir}/angle.txt'): 
    print('File already exists')
    exit()

file = f'{dir}/sim.lammpstrj'

dz = 1                     # bin size 
begin_frame = 100

pipeline = import_file(file)

pipeline.modifiers.append(ClusterAnalysisModifier(
    cutoff = 0.9, sort_by_size = True))
pipeline.modifiers.append(ExpressionSelectionModifier(
    expression = 'Cluster != 1'))
pipeline.modifiers.append(DeleteSelectedModifier())

num_frames = pipeline.source.num_frames

result = np.zeros(16)-1
for frame in range(begin_frame, num_frames):
    print(frame, end='\r')
    data = pipeline.compute(frame)

    positions = data.particles_.positions_

    idz = np.floor(positions[:,2]/dz).astype('int32')
    # Fix id of edge cases
    idz[idz < 0] = 0
    numz = idz.max()+1
    count = np.zeros(numz)
    binsx = {i:[] for i in range(numz)}
    binsy = {i:[] for i in range(numz)}
    center = np.zeros((numz,2))
    for p, i in enumerate(idz):
        px, py = positions[p,:2]
        center[i] += [px, py]
        count[i] += 1
        binsx[i].append(px)
        binsy[i].append(py)

    radii = np.zeros(numz)
    for i in range(0, numz):
        center[i,0] /= count[i]
        center[i,1] /= count[i]
        binsx[i] = np.array(binsx[i]) - center[i,0]
        binsy[i] = np.array(binsx[i]) - center[i,0]
        radius = np.sqrt(binsx[i]**2 + binsy[i]**2)
        radius = radius[radius > radius.max()- 1.5]
        radii[i] = radius.mean()
    result[:numz] += radii
print('Last frame: ', frame)

result /= (num_frames-begin_frame+1)    

result = result[result > -1]
numz = len(result)
radmin = np.flip(result)
function = np.concatenate((-radmin+2*result[0], result[1:]))
xx = np.linspace(-numz,numz,2*numz-1)*dz
cs = CubicSpline(xx,function)

value = np.arctan2(1,cs(0,1))*180/np.pi
print('Angle is ', value)

if frame < 290:
    print('Enough frames')
    exit()

with open(f'{dir}/angle.txt', 'x') as fd:
    fd.write(str(value))




