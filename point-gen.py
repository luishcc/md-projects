import numpy as np
import sys
import os
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib as mpl



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius
        self.area = np.pi * self.radius**2

    def get_random_point(self):
        p = np.random.random() * 2 * np.pi
        r = self.radius * np.sqrt(np.random.random())
        x = np.cos(p) * r
        y = np.sin(p) * r
        return Point(x, y)

def perturbation_radius(amp, wave_length, z):
    return 1 + amp * np.cos(2 * np.pi * z / wave_length)


origin = Point(0, 0)
num_circles = 20
height = 60
dist_circle = height/num_circles
r_0 = 6
circles_zcoord = np.linspace(0, height, num_circles)

xx = []
yy = []
zz = []
for z in circles_zcoord:
    rad = r_0 * perturbation_radius(0.1, height, z)
    print(z, rad)
    circle = Circle(origin, rad)
    for i in range(0, 500):
        p_rand = circle.get_random_point()
        z_rand = z - 0.5 * dist_circle + dist_circle*np.random.random()
        xx.append(p_rand.x)
        yy.append(p_rand.y)
        zz.append(z_rand)


fig = plt.figure()
ax = fig.gca(projection='3d')

x_scale=1
y_scale=1
z_scale=5

scale=np.diag([x_scale, y_scale, z_scale, 1.0])
scale=scale*(1.0/scale.max())
scale[3,3]=1.0

def short_proj():
  return np.dot(Axes3D.get_proj(ax), scale)

ax.get_proj=short_proj
ax.grid(False)
plt.axis('off')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.plot(xx, yy, zz, 'k.')
plt.show()
