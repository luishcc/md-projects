import numpy as np
from scipy.special import iv, kv

def grow_lin(x, h, sigma, mu):
    i0 = iv(0,x)
    i1 = iv(1,x)
    k0 = kv(0,x)
    k1 = kv(1,x)
    frac = i1/i0
    prod1 = x**2*h**2*i0*k0
    prod2 = i1*k0+mu*i0*k1
    prod3 = sigma*frac*(x-x**3)
    return (prod1/prod2 - prod3)


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
x = np.linspace(0.0001,1,num)

lw = 2.5
ax.plot(x, grow_lin(x, 1, 1, 1), 'k-', linewidth=lw, label=f'111')
ax.plot(x, grow_lin(x, 10, 1, 1), 'k--', linewidth=lw, label=f'h 10')
ax.plot(x, grow_lin(x, .1, 1, 1), 'k-.', linewidth=lw, label=f'h 0.1')

ax.plot(x, grow_lin(x, 1, 10, 1), 'b--', linewidth=lw, label=f's 10')

ax.plot(x, grow_lin(x, 1, 1, 10), 'g--', linewidth=lw, label=f'm 10')
ax.plot(x, grow_lin(x, 1, 1, 0.1), 'g-.', linewidth=lw, label=f'm 0.1')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$\omega / \omega_0$')
ax.legend(loc='upper left', frameon=False)
ax.grid(True)
ax.set_ylim(-1,1)

plt.tight_layout()
# fig.savefig('ch3fig2.pdf', dpi=dpi)

plt.show()
