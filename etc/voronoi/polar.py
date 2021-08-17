import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d



posx = []
posy = []
for r in range(6):
    N = round(np.pi*(r+1))
    theta = 2*np.pi / N
    for p in range(N):
        posx.append((r+0.5)*np.cos(p*theta+0.5*theta))
        posy.append((r+0.5)*np.sin(p*theta+0.5*theta))

size = len(posx)
point = np.zeros((size, 2))

for i in range(size):
    point[i,0] = posx[i]
    point[i,1] = posy[i]

voro  = Voronoi(point)

fig = voronoi_plot_2d(voro)

plt.figure(2)
plt.plot(posx, posy, 'ko')
plt.show()
