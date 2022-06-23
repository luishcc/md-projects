import numpy as np

import itertools

import sys
import os

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib as mpl

pi = np.pi

class Molecule:
    id_iter = itertools.count()
    def __init__(self, atoms):
        self.atoms = atoms
        self.id = next(self.id_iter) + 1


class Atom:
    id_iter = itertools.count()
    def __init__(self, x, y, type=1):
        self.x = x
        self.y = y
        self.type = type
        self.id = next(self.id_iter) + 1


class Circle:
    def __init__(self, origin, radius, num):
        self.origin = origin
        self.radius = radius
        self.points = self.get_points(num)
        self.atoms = []

    def get_points(self, num):
        p = np.linspace(0,2*pi, num)
        x = np.cos(p) * self.radius
        y = np.sin(p) * self.radius
        lst = []
        for i, j in zip(x,y):
            lst.append(np.array([i,j]))
        return lst

    def add_chain(self, num, d):
        for p in self.points:
            norm = np.sqrt(p[0]**2+p[1]**2)
            vect = d*p/norm
            self.atoms.append(Atom(p[0], p[1]))
            for i in range(1,num+1):
                xy = i*d*vect + p
                self.atoms.append(Atom(xy[0], xy[1], type=2))



origin = (0, 0)
num_circles = 10
height = 60
dist_circle = height/num_circles
r0 = 6
circles_zcoord = np.linspace(0, height, num_circles)

xx = []
yy = []
zz = []

for z in circles_zcoord:
    print(z, r0)
    circle = Circle(origin, r0, 10)
    circle.add_chain(3, 1)
    for i in circle.atoms:
        xx.append(i.x)
        yy.append(i.y)
        zz.append(z)




fig = plt.figure()
ax = fig.gca(projection='3d')
#
# x_scale=1
# y_scale=1
# z_scale=5
#
# scale=np.diag([x_scale, y_scale, z_scale, 1.0])
# scale=scale*(1.0/scale.max())
# scale[3,3]=1.0

# def short_proj():
#   return np.dot(Axes3D.get_proj(ax), scale)
#
# ax.get_proj=short_proj
ax.grid(False)
plt.axis('off')
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.plot(xx, yy, zz, 'k.')
plt.show()
