import numpy as np
import os

from write import DataFile


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

class Point:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def set_z(self, value):
        self.z = value
        return

class Circle:
    def __init__(self, radius):
        self.radius = radius
        self.area = np.pi * self.radius**2

    def get_random_point(self):
        p = np.random.random() * 2 * np.pi
        r = self.radius * np.sqrt(np.random.random())
        x = np.cos(p) * r
        y = np.sin(p) * r
        return Point(x, y)

def perturbation_radius(amp, length, z):
    return 1 + amp * np.cos(2 * np.pi * z / length)

if __name__ == '__main__':

    density = 6.9
    r0 = 6.0

    wave_number_r = 0.35
    wave_length = (2*np.pi*r0)/wave_number_r
    perturbation_amp = 0.01*r0

    box = Box(6*r0, 6*r0, wave_length)

    num_circles = 300
    num_point = 200
    dist_circle = wave_length/num_circles
    circles_zcoord = np.linspace(0, wave_length, num_circles)


    positions = []

    rad = r0 * perturbation_radius(perturbation_amp, wave_length, 0)
    circle = Circle(rad)
    for i in range(num_point):
        p_rand = circle.get_random_point()
        p_rand.set_z(0.5 * dist_circle*np.random.random())
        positions.append(p_rand)
    for z in circles_zcoord[1:-1]:
        rad = r0 * perturbation_radius(perturbation_amp, wave_length, z)
        circle = Circle(rad)
        for i in range(0, num_point):
            p_rand = circle.get_random_point()
            p_rand.set_z(z - 0.5 * dist_circle + dist_circle*np.random.random())
            positions.append(p_rand)
    rad = r0 * perturbation_radius(perturbation_amp, wave_length, circles_zcoord[-1])
    circle = Circle(rad)
    for i in range(num_point):
        p_rand = circle.get_random_point()
        p_rand.set_z(circles_zcoord[-1] - 0.5 * dist_circle*np.random.random())
        positions.append(p_rand)


    atoms = Atoms(positions, density)

    data = DataFile(box, atoms)
    data.write_file('test', os.getcwd())
