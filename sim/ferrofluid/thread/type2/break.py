import os
import sys
import numpy as np

from ovito.io import *

dir = sys.argv[1]
print(dir)
if os.path.isfile(f'{dir}/breaktime.txt'): 
    print('File already exists')
    exit()

file = f'{dir}/sim.lammpstrj'

dz = .8                     # bin size 
begin_frame = 100

pipeline = import_file(file)
num_frames = pipeline.source.num_frames
if num_frames < 400:
    print('Not Enough frames')
    exit()

def check_snap(frame):
    data = pipeline.compute(frame)

    lz = data.cell.matrix[2,2]   
    num_z = round(lz/dz)
    size_z = lz / (num_z)

    positions = data.particles_.positions_

    radii = np.sqrt(positions[:,0]**2 + positions[:,1]**2)
    positions = positions[radii < 3]

    idz = np.floor(positions[:,2]/size_z).astype('int32')
    
    # Fix id of edge cases
    idz[idz < 0] = 0
    idz[idz > num_z-1] = num_z-1

    num_bins = len(np.unique(idz))

    return num_bins>=num_z

a = 1
b = num_frames-1
fa = check_snap(a)
fb = check_snap(b)

MAX = 1000
N = 0
while N < MAX:
    print(N)
    N+=1
    c = (b + a) // 2
    fc = check_snap(c)
    print(a, fa, b, fb, c, fc)

    if c == a or c == b:
        print('a: ', a, 'b: ', b)
        break

    if fc == fa:
        a = c
    else:
        b = c

with open(f'{dir}/breaktime.txt', 'x') as fd:
    fd.write(str(b))
