import numpy as np
import matplotlib.pyplot as plt

import cmath


idr = [0, 1, 2, 3, 4, 5]
p = []
nang = []
wall = {}

for i in idr:

  n = round(np.pi*(2*i+1))
  dp = 2*np.pi / n
  lst = []

  for j in range(n):
    p.append(i+0.5)
    nang.append((j*dp + dp*0.5))
    lst.append((j*dp))
    wall[i] = lst
    
x = []
y = []

for r, a in zip(p, nang):
  x.append( r * np.cos(a))
  y.append( r * np.sin(a))

wall_x = []
wall_xx = []
wall_y = []
wall_yy = []

for key, value in wall.items():
  for ang in value:
    wall_x.append(key*np.cos(ang))
    wall_xx.append((key+1)*np.cos(ang))    
    wall_y.append(key*np.sin(ang))
    wall_yy.append((key+1)*np.sin(ang))    
  
    

fig, ax = plt.subplots()

ax.plot(x,y,'k.')

for i in range(len(wall_x)):
  ax.plot([wall_x[i], wall_xx[i]], [wall_y[i], wall_yy[i]], 'k-')

for i in range(len(idr)+1):
  circle1 = plt.Circle((0, 0), i, color='k', fill=False)
  #plt.gca().add_patch(circle1)
  ax.add_patch(circle1)

ax.set_xlim(-6.5, 6.5)
ax.set_box_aspect(1)
ax.set_yticklabels([])
ax.set_xticklabels([])
fig.set_dpi(200)

plt.show()
  

