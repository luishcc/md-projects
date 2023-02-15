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

path_to_data = '/home/luishcc/hdd/free_thread_old/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
# path_to_data = '/home/luishcc/hdd/'


def get_snap(dir, exact=True):
    with open(dir+'/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

R = [2,4,6]
ratio = 48
A = [-40,-50,-60,-70,-80,-85,-90]

radii = {2:[1.55, 1.5, 1.45, 1.41, 1.39, 1.36, 1.3],
           4:[3.2, 3.1, 3, 3, 2.9, 2.85, 2.8],
           6:[5.3, 5, 4.8, 4.5, 4.4, 4.35, 4.3]}


sum = 0
sumsq = 0

fig, ax = plt.subplots(1,1)


###############

color = {2:'red', 4:'green', 6:'blue'}
marker = {2:'s', 4:'x', 6:'o'}
lstyle = {2:'-.', 4:'--', 6:'-'}

for r in R:
    avg = []
    var = []
    for i, a in enumerate(A):
        n = 1
        sum = 0
        sumsq = 0
        data_case_dir = f'R{r}_ratio{ratio}_A{abs(a)}/1'
        dir = path_to_data + data_case_dir
        print(os.path.isdir(dir))
        while os.path.isdir(dir):
            snap = get_snap(dir)
            sum += snap
            sumsq += snap**2
            n += 1
            data_case_dir = f'R{r}_ratio{ratio}_A{abs(a)}/{n}'
            dir = path_to_data + data_case_dir

        avg.append((sum/(n-1))*(r/radii[r][i]))
        # avg.append((sum/(n-1))/(radii[r][i]**2))
        var.append(sumsq/(n-1) - (sum/(n-1))**2)

    ax.errorbar(A, avg, yerr = [np.sqrt(v) for v in var],
            linewidth=1., fmt=marker[r],ecolor = color[r],markersize=6,
            color=color[r], markerfacecolor='none', capsize=2.5, capthick=0.6,
            label=rf'$R_0={r}$')


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
