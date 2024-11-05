import numpy as np

import matplotlib as mpl


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)


def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)

oh = np.linspace(0.1, 2.60, 10000)
x = np.zeros(len(oh))

x = func(oh)

rho = [7.65, 8.30, 8.95, 9.6, 9.92, 10.24]
rho2 = [6.05, 6.9, 7.7, 8.4, 9.1, 9.5, 9.8]
rho3 = [ 6.75, 7.65, 8.30, 8.95, 9.6, 9.92, 10.24]


lr = {}
invlr = {}

lr[6] = [np.cbrt(1/i) for i in rho3]
invlr[6] = [1/i for i in lr[6]]
lr[4] = [np.cbrt(1/i) for i in rho3]
invlr[4] = [1/i for i in lr[4]]
lr[2] = [np.cbrt(1/i) for i in rho3]
invlr[2] = [1/i for i in lr[2]]

oh_r = {}
oh_r[6] = [.198, .266, .321, .451, .704, .901, 1.14]
oh_r[4] = [.243, .325, .393, .552, .863, 1.10, 1.39]
oh_r[2] = [.345, .460, .556, .781, 1.22, 1.56, 1.96]



A = [ 40, 50, 60, 70, 80, 85, 90]

R = [2, 4, 6]
scale_r = {2:.85, 4:.85, 6:.8}
radii_r = {2:[1.55, 1.5, 1.45, 1.41, 1.39, 1.36, 1.3],
           4:[3.2, 3.1, 3, 3, 2.9, 2.85, 2.8],
           6:[5.3, 5, 4.8, 4.5, 4.4, 4.35, 4.3]}
ratio = 48

oh_r[6] = [(oh**2*6/ri)**.5 for ri, oh in zip(radii_r[6], oh_r[6])]
oh_r[4] = [(oh**2*4/ri)**.5 for ri, oh in zip(radii_r[4], oh_r[4])]
oh_r[2] = [(oh**2*2/ri)**.5 for ri, oh in zip(radii_r[2], oh_r[2])]


q = {}
qinv = {}
q_var = {}
for r in R:
    q[r]=[]
    qinv[r]=[]
    q_var[r]=[]
    for i, a in enumerate(A):
        file = f'../analysis/density_correlation/peak/R{r}_ratio{ratio}_A{a}-peak.csv'
        try:
            with open(file, 'r') as fd:
                fd.readline()
                line = fd.readline().split(',')
                q[r].append(float(line[0]) * 2 * np.pi * radii_r[r][i])
                qinv[r].append(1/(float(line[0]) *  radii_r[r][i]))
                q_var[r].append(float(line[1]) * ( 2 * np.pi * radii_r[r][i])**2)
        except Exception as e:
            print(e)
            continue

import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (1*side, .6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, ax = plt.subplots(1,1)


q[2] = [(i*21)/20 for i in q[2]]
q_var[2] = [(i*21)/20 for i, j in zip(q_var[2],q[2])]

ax.plot(oh, x, label='Theory', linewidth=2.5, color='k', linestyle='--' )

ax.set_ylabel('$x$')
ax.set_xlabel(r'Oh')
ax.set_ylim(0.22, 0.69)
ax.set_xlim(0.06, 2.5)


print(oh_r, q, q_var)

color = {2:'red', 4:'green', 6:'blue'}
marker = {2:'s', 4:'^', 6:'o'}
lstyle = {2:'-.', 4:'--', 6:'-'}

for r in R:
    # print(r)
    # print(oh_r[r], q[r], q_var[r])
    ax.errorbar(oh_r[r], q[r], yerr = 2*np.sqrt(np.array(q_var[r])/30), 
                fmt='none', ecolor = color[r], color=color[r], 
                label=f'$R_0={r}$', capsize=5, linewidth=2)
    ax.scatter(oh_r[r], q[r], marker=marker[r], edgecolor=color[r], 
               label=f'$R_0={r}$', s=80, linewidth=2, c='none')

    a2 = np.linspace(0.0, 0.8, 100)


from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax.legend(handles, labels, loc='upper right', columnspacing=0.8,  handletextpad=.3,
frameon=False, ncol=2, fontsize=15, handlelength=2.5)

fig.tight_layout()
plt.savefig('ch3fig6.pdf', dpi=dpi, bbox_inches='tight')

plt.show()
