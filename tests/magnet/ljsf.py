import numpy as np 
import matplotlib.pyplot as plt


r = np.linspace(.2, 1.5, 100000)

def ln(r):
    n = 1000
    delta = 0.2
    dh = 1
    temp = n/(2*delta)*(dh - r * (np.log(dh/r) + 1))
    temp = temp[(dh-2*delta) < r ]
    r = r[(dh-2*delta) < r ]
    return r[r < dh], temp[r < dh]

def ljsf(r):
    sig = 2**(-1/6)
    ep = 1
    s6 = (sig/r)**6
    s12 = s6**2
    temp = 4*ep*(s12-s6 + (6*sig**12-3*sig**6)*(r/sig)**2-7*sig**12+4*sig**6)
    return r[r < 1], temp[r < 1]

def ljquart(r):
    sig = 2**(-1/6)
    ep = 1
    s6 = (sig/r)**6
    s12 = s6**2
    temp = 4*ep*(s12-s6 + 0.25)
    return  r[r < 1], temp[r < 1]

fig, ax = plt.subplots(1,1)

ax.plot(*ln(r), 'k-', label='ln')
ax.plot(*ljquart(r), 'b--', label='ljquart')
ax.plot(*ljsf(r), 'y-.', label='ljsf')
ax.set_ylim(-10, 100)

ax.legend()

plt.show()
