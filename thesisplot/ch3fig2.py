import numpy as np
from scipy.special import iv

def grow_lin(x):
    frac = iv(1,x)/iv(0,x)
    return np.sqrt(frac*(x-x**3))

def growth_rate(x, oh):
    x2 = x**2
    x4 = x2**2
    t1 = 0.5*(x2-x4)
    t2 = 2.25*oh**2*x4
    t3 = 1.5*oh*x2
    return np.sqrt(t1+t2)-t3

def max_growth(oh):
    return np.sqrt(1 / (2+np.sqrt(18)*oh))

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (1.*side, .7*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, ax = plt.subplots(1,1)

num=100
x = np.linspace(0,1,num)

lw = 2.5

ax.plot(x, growth_rate(x,0.01), 'b--', linewidth=lw, label=f'Oh=0.01')
ax.plot(x, growth_rate(x,.1), 'r-.', linewidth=lw, label=f'Oh=0.1')
ax.plot(x, growth_rate(x,1), 'g', linestyle='dotted', linewidth=lw, label=f'Oh=1.0')
ax.plot(x, grow_lin(x), 'k-', linewidth=lw, label=f'Inviscid')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$\omega / \omega_0$')
ax.legend(loc='upper left', frameon=False)

plt.tight_layout()
fig.savefig('ch3fig2.pdf', dpi=dpi)

plt.show()
