import numpy as np
import os


class Point:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

class Atoms:
    def __init__(self, points, density):
        self.number = len(points)
        self.positions = points
        self.density = density
        return

class Box:
    def __init__(self, lx, ly, lz):
        self.xlo = -lx/2.
        self.xhi = lx/2.
        self.ylo = -ly/2.
        self.yhi = ly/2.
        self.zlo = 0
        self.zhi = lz



