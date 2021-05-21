import numpy as np
import sys
import os
import random
import math
import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

class Circle:
    def __init__(self, origin, radius):
        self.origin = origin
        self.radius = radius

origin = Point(0, 0)
radius = 10
circle = Circle(origin, radius)


xx=[]
yy=[]

num = 1000
for i in range(0, num):
    p = random.random() * 2 * math.pi
    r = circle.radius * math.sqrt(random.random())
    x = math.cos(p) * r
    y = math.sin(p) * r
    xx.append(x)
    yy.append(y)
    print(x, y)

plt.figure(1)
plt.plot(xx, yy, 'k.')
plt.show()
