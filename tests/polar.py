import numpy as  np

n = 10

r = [1]*n
phi = np.linspace(0, 2*np.pi, n, endpoint=False )

def pol2cart(r, phi):
    x = r*np.cos(phi)
    y = r*np.sin(phi)
    return x, y

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

f = [0.1, 0]

x = []
y = []
for a, b in zip(r,phi):
    xx, yy = pol2cart(a,b)
    x.append(xx)
    y.append(yy)


def convert(v, p):
    phi = np.arctan2(p[1], p[0])
    a = v[0]*np.sin(phi+np.pi/2) - v[1]*np.cos(phi+np.pi/2)
    b = v[0]*np.cos(phi+np.pi/2) + v[1]*np.sin(phi+np.pi/2)
    return a, b


def convert2(v, p):
    phi = np.arctan2(p[1], p[0])
    a = v[0]*np.cos(phi) + v[1]*np.sin(phi)
    b = -v[0]*np.sin(phi) + v[1]*np.cos(phi)
    return a, b


for a, b in zip(x,y):
    ft, fr = convert2(f, [a,b])
    print(ft, fr)
    ax.text(a, b+0.05, f'({round(ft, 3)}, {round(fr, 3)})')
    ax.plot([a, a+f[0]],[b, b+f[1]], 'b->')
ax.plot(x, y, 'ko')


plt.show()
