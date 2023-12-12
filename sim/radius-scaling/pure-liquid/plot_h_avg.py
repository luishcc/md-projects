import matplotlib.pyplot as plt 
import numpy as np

def run_snapshot(dir, time):
    # Read surface profile radius from .dat file
    with open(f'{dir}/surface_profile/{time}.dat') as fd:
        line = fd.readline().split(' ')
        dz = float(line[5].split('=')[1])
        num = int(line[6].split('=')[1])
        shape = np.ones(num)*-1
        for id, line in enumerate(fd):
            line = line.split(' ')
            radius = float(line[1])
            shape[id] = radius  
    return shape, dz

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap


path = '/home/luishcc/hdd/radius_scaling/low-Oh'
# path = '/home/luishcc/hdd/radius_scaling/high-Oh'

num_sim = 20
shapes = []
bulk = []
surface = []
for i in range(num_sim):
    dir = f'{path}/{i+1}'
    time = get_breaktime(dir)-1
    shape, dz = run_snapshot(dir, time)
    
    # dist = shape.argmax()
    # shape = np.roll(shape, -dist)
    # flip = shape.argmin() < len(shape)/2    
    # if flip: 
    #     shape = np.flip(shape)
    
    dist = shape.argmin()-int(len(shape)/2)
    shape = np.roll(shape, -dist)
    flip = shape.argmin() - shape.argmax() > 0
    if flip: 
        shape = np.flip(shape)
    shapes.append(shape)

ids = np.linspace(0.5,len(shapes[0])+0.5, len(shapes[0]))*dz
# ids = np.linspace(-1,1, len(shapes[0]))

fig, ax = plt.subplots(1,1)

sum = np.zeros(len(shapes[0]))
sumsq = np.zeros(len(shapes[0]))
for shape in shapes:
    sum += shape
    sumsq += shape**2
    # ax.plot(ids, shape, 'c--')

avg = sum/num_sim
var = sumsq/num_sim - avg**2
std = np.sqrt(var)

ax.plot(ids, avg, 'k-')
ax.fill_between(ids, avg-std, avg+std, color='gray', alpha = 0.5)
ax.plot(ids, -avg, 'k-')
ax.fill_between(ids, -avg-std, -avg+std, color='gray', alpha = 0.5)
ax.set_aspect('equal', adjustable='box')


plt.show()
    