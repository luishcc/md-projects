import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)



paths_list = ['phase-mdpd/4',
             'phase-mdpd/25',
             'phase-martini/5',
             'phase-martini/25']



Sq_values = []

for path in paths_list:
    q = []
    sq = []
    with open(f'{path}/scatter.dat', 'r') as fd:
        fd.readline()
        for line in fd:
            line = fd.readline().split(' ')
            q.append(float(line[0]))
            sq.append(float(line[1]))
    Sq_values.append(sq)


fig, ax = plt.subplots(1,1)


#ax.errorbar([0]+sc_lst, [72]+gamma_lst, yerr = [std_lst[0]*0.9]+std_lst, fmt='o',
#ecolor = 'black', capsize= 2, capthick=1,color='black', label=r'MDPD')

ax.plot(q, Sq_values[0], 'rP', label=r'MDPD 5\%')
ax.plot(q, Sq_values[1], 'ko', label=r'MDPD 25\%')
ax.plot(q, Sq_values[2], 'c^', label=r'MD 5\%')
ax.plot(q, Sq_values[3], 'bs', label=r'MD 25\%')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_xlim(0.009,0.7)
ax.set_ylim(0.002,4)

ax.set_xlabel(r'q [\AA$^{-1}$]')
ax.set_ylabel(r'I(q) [.]')

lines, labels = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='lower left', frameon=False)

plt.tight_layout()
plt.savefig('scatter.pdf', dpi=dpi)
plt.show()
