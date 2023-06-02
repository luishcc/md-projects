import numpy as np

import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.5*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt

sf = [0.5, 1.0, 1.6, 1.8, 2.0, 2.3, 2.6, 2.9, 3.4]

surf_tension = [6.16, 4.60, 3.09, 2.69, 2.67, 2.65, 2.61, 2.66, 2.66]

R=8

rho = 5.8
sf2 = [8*i/(i*8+R*rho) for i in sf]
# sf2 = [8*i/R for i in sf]

q = []
qinv = []
q_var = []

for i, a in enumerate(sf):
    # file = f'peak/R{R}_{a}-peak.csv'
    file = f'R{R}_{a}-peak.csv'
    try:
        with open(file, 'r') as fd:
            fd.readline()
            line = fd.readline().split(',')
            q.append(float(line[0]) * 2 * np.pi * R*1)
            qinv.append(1/(float(line[0]) *  R))
            q_var.append(float(line[1]) * ( 2 * np.pi * (R*1)**2)/1)
    except Exception as e:
        print(e)
        continue

fig, ax = plt.subplots(1,1)

# plt.title('Reduced Wavenumber')
ax.set_ylabel('$\chi$')
ax.set_xlabel(r'C $[N_s/V]$')
# ax.set_ylim(0.22, 0.69)
# ax.set_xlim(0.06, 2.31)

ax.errorbar([0]+sf2, [0.67]+q, yerr = np.sqrt([0.001/1]+q_var), fmt='.',
ecolor = 'black', color='black', label=f'$R_0={R}$',
capsize=3, markerfacecolor='none')

import matplotlib as mpl
from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
# ax.legend(handles, labels, loc='upper right', columnspacing=0.6,  handletextpad=.1,
# frameon=False, ncol=2, fontsize=12, handlelength=1.5)

# fig.savefig('surfactant.png', bbox_inches='tight')
# plt.show()

fig, ax = plt.subplots(1,1)

def chi(oh):
    return 1/(np.sqrt(2+np.sqrt(18)*oh))

def oh(mu, gamma, rho, r):
    return mu/np.sqrt(rho*gamma*r)

x = np.linspace(1, 8, 100)
y = chi(oh(3.8, x, 6, R))

ax.plot(surf_tension, q, 'ko', label='Simulations')
ax.plot(x,y, 'k--', label=r'Theory ($\mu$, $\rho$ of pure liquid)')
ax.set_xlabel(r'$ \gamma $ [MDPD units]')
ax.set_ylabel(r'$ \chi $')
ax.legend(frameon=False)

plt.show()