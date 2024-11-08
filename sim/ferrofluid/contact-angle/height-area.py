import os
import sys
import numpy as np
from scipy.interpolate import CubicSpline

from ovito.io import *
from ovito.modifiers import *

dir = sys.argv[1]
print(dir)
if os.path.isfile(f'{dir}/height.txt') and os.path.isfile(f'{dir}/area.txt'): 
    print('Files already exist')
    exit()

file = f'{dir}/sim.lammpstrj'

# dir = os.getcwd()
# file = '0.10/2/3.00/sim.lammpstrj'

dz = 1                  # bin size 
begin_frame = 100

pipeline = import_file(file)
num_frames = pipeline.source.num_frames
if num_frames < 300:
    print('Not Enough frames')
    exit()

pipeline.modifiers.append(ClusterAnalysisModifier(
    cutoff = 0.9, sort_by_size = True))
pipeline.modifiers.append(ExpressionSelectionModifier(
    expression = 'Cluster != 1'))
pipeline.modifiers.append(DeleteSelectedModifier())

result = np.zeros(18)-1
height = np.zeros(num_frames-begin_frame+1)
area = np.zeros(num_frames-begin_frame+1)
for frame in range(begin_frame, num_frames):
    print(frame, end='\r')
    data = pipeline.compute(frame)

    positions = data.particles_.positions_
    centerx = np.mean(positions[:,0])
    centery = np.mean(positions[:,1])
    
    positions -= np.array([centerx, centery, 0])
    x = positions[:,0]  
    y = positions[:,1]  
    z = positions[:,2]  

    height[frame-begin_frame] = np.mean(np.sort(z)[::-1][:10])

    radii = np.sqrt(x**2+y**2)

    contact_atoms = positions[z<dz]
    radii = radii[z<dz]
    edge = radii.max()-1.5
    radii = np.mean(radii[radii>edge])

    # print(centerx, centery, edge)

    area[frame-begin_frame] = np.pi*radii*2

print('Last frame: ', frame)


print('height is ', height.mean(), height.std())
print('area is ', area.mean(), area.std())

try:
    with open(f'{dir}/height.txt', 'x') as fd:
        fd.write(f'{str(height.mean())}\n')
        fd.write(str(height.std()))
except: pass

try:
    with open(f'{dir}/area.txt', 'x') as fd:
        fd.write(f'{str(area.mean())}\n')
        fd.write(str(area.std()))
except: pass






