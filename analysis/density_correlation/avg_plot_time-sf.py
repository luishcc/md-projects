import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (.7*side, .45*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

path_to_data = '/home/luishcc/hdd/surfactant/new/'

def get_snap(dir, exact=True):
    with open(dir+'/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

R = 8
A = [0.5, 1.0, 1.6, 1.8, 2.0, 2.3, 2.6, 2.9, 3.4]
diff = [50, 50, 50, 100, 100, 100, 150, 150, 150]


sum = 0
sumsq = 0

fig, ax = plt.subplots(1,1)


###############

avg = []
var = []
for i, a in enumerate(A):
    n = 1
    sum = 0
    sumsq = 0
    data_case_dir = f'R{R}-{a}/1'
    dir = path_to_data + data_case_dir
    print(os.path.isdir(dir))
    while os.path.isdir(dir):
        snap = get_snap(dir)+diff[i]
        sum += snap
        sumsq += snap**2
        n += 1
        data_case_dir = f'R{R}-{a}/{n}'
        dir = path_to_data + data_case_dir

    avg.append((sum/(n-1)))
    # avg.append((sum/(n-1))/(radii[r][i]**2))
    var.append(sumsq/(n-1) - (sum/(n-1))**2)

ax.errorbar(A, avg, yerr = [np.sqrt(v) for v in var],
        linewidth=1., fmt='o',ecolor = 'black',markersize=6,
        color='black', markerfacecolor='none', capsize=2.5, capthick=0.6,
        label=rf'$R_0$')


# ax.set_xlim(0,0.08)

ax.set_ylabel(r'$t_b$')
ax.set_xlabel(r'$A$')

from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax.legend(handles, labels, frameon=False)

fig.tight_layout()
# plt.savefig('figSM3.pdf', dpi=dpi, bbox_inches='tight')
plt.show()
