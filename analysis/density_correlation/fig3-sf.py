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

sf = [1.0, 1.6, 2.0, 2.3, 2.6]
R=8

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
            q.append(float(line[0]) * 2 * np.pi * R)
            qinv.append(1/(float(line[0]) *  R))
            q_var.append(float(line[1]) * ( 2 * np.pi * R**2))
    except Exception as e:
        print(e)
        continue

fig, ax = plt.subplots(1,1)

# plt.title('Reduced Wavenumber')
ax.set_ylabel('$\chi$')
ax.set_xlabel(r'N_s/A_s')
# ax.set_ylim(0.22, 0.69)
# ax.set_xlim(0.06, 2.31)


ax.errorbar(sf, q, yerr = np.sqrt(q_var), fmt='.',
ecolor = 'black', color='black', label=f'$R_0={R}$',
capsize=3, markerfacecolor='none')

import matplotlib as mpl
from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
# ax.legend(handles, labels, loc='upper right', columnspacing=0.6,  handletextpad=.1,
# frameon=False, ncol=2, fontsize=12, handlelength=1.5)


plt.show()
