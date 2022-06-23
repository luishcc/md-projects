import numpy as np


types = {head:[], tail:[]}

r0 = 0.64
a0 = 160

num_h = 1
num_t = 3

theta = np.linspace( 0 , 2 * np.pi , 150 )
radius = 0.4

a = radius * np.cos( theta )
b = radius * np.sin( theta )
