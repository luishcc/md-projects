import numpy as np
import matplotlib.pyplot as plt

from ovito.io import *
from ovito.modifiers import *

# file = 'dump.angle1'
# file = 'dump.angle2'
file = 'dump.angle3'

pipeline = import_file(file)

pipeline.modifiers.append(ClusterAnalysisModifier(
    cutoff = 0.9, sort_by_size = True))
pipeline.modifiers.append(ExpressionSelectionModifier(
    expression = 'Cluster != 1'))
pipeline.modifiers.append(DeleteSelectedModifier())

# surf_mod = ConstructSurfaceModifier(
#     method = ConstructSurfaceModifier.Method.AlphaShape,
#     radius = 0.7,
#     select_surface_particles = True)
# pipeline.modifiers.append(surf_mod)

# pipeline.modifiers.append(InvertSelectionModifier())
# pipeline.modifiers.append(DeleteSelectedModifier())


num_frames = pipeline.source.num_frames
data = pipeline.compute(0)

dz = 1                     # bin size 
begin_frame = 50

result = np.zeros(14)
for frame in range(begin_frame, num_frames):
    print(frame)
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
    # center /= count 

    radii = np.zeros(numz)
    for i in range(0, numz):
        center[i,0] /= count[i]
        center[i,1] /= count[i]
        binsx[i] = np.array(binsx[i]) - center[i,0]
        binsy[i] = np.array(binsx[i]) - center[i,0]
        radius = np.sqrt(binsx[i]**2 + binsy[i]**2)
        radius = radius[radius > radius.max()- 1.5]
        # radii[i] = np.sqrt(binsx[i]**2 + binsy[i]**2).mean()
        radii[i] = radius.mean()
    result[:numz] += radii

result /= (num_frames-begin_frame+1)    


###################################################################################
# Plotting results


import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.7*side, 0.5*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)



numz = len(result)
x = np.linspace(0,numz,numz) * dz
xmin = np.linspace(-numz,0, numz) * dz

radmin = np.flip(result)

function = np.concatenate((-radmin+2*result[0], result[1:]))

xx = np.linspace(-numz,numz,2*numz-1)*dz

from scipy.interpolate import CubicSpline
cs = CubicSpline(xx,function)

fig, ax = plt.subplots(1,1)
# ax.plot(x, result)
# ax.plot(xmin, -radmin+2*result[0])

ax.plot(np.linspace(-numz,numz,2*numz-1)*dz, function, 'ko')

x1 = np.linspace(-numz,numz,1000)
ax.plot(x1, cs(x1), 'b--')
ax.plot(x1, cs(x1,1), 'k-.')
ax.axes.set_aspect('equal')

ax.set_ylim(0,12)
ax.set_xlim(-10,10)
# ax.legend(frameon=False, loc='center left', fontsize=10)

print(np.arctan2(1,cs(0,1))*180/np.pi)

plt.show()

