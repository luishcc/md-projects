import numpy as np

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

import matplotlib.pyplot as plt

sf = [0.5, 1.0, 1.6, 1.8, 2.0, 2.3, 2.6, 2.9, 3.4]

surf_tension = [6.16, 4.60, 3.09, 2.69, 2.67, 2.65, 2.61, 2.66, 2.66]

R=8

rho = 5.8
# sf2 = [8*i/(i*8+R*rho) for i in sf]
sf2 = [8*i/R for i in sf]

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

ax.set_ylabel(r'$\chi$ [$\cdot$]')
ax.set_xlabel(r'C $[N_t/A_s]$')
ax.set_ylim(0., 0.72)
# ax.set_xlim(0.06, 2.31)

ax.errorbar([0]+sf2, [0.67]+q, yerr = np.sqrt([0.001/1]+q_var), fmt='o',
ecolor = 'black', color='black', label=f'$\chi$', capsize=3, markerfacecolor='none')

import matplotlib as mpl
from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]

ax.plot([1.8, 1.8], [.3, .6], 'k--')
ax.annotate('CMC', xy=(1.85, .55), xytext=(2.3, 0.65),
            arrowprops=dict(facecolor='black', shrink=0.05))
############################################################
############################################################
# axx = ax.twinx()
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition)
axx = plt.axes([0,0,1,1])
ip = InsetPosition(axx, [0.16,0.2,0.6,0.53])
axx.set_axes_locator(ip)
axx.set_ylabel(r'$t_{break-up}$ [$\tau$]')
axx.set_xlabel(r'C $[N_t/A_s]$')
#############
import os
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
axx.errorbar([0]+A, [40]+avg, yerr = [np.sqrt(var[0])]+[np.sqrt(v) for v in var], fmt='x',
             ecolor = 'red', color='red', markerfacecolor='none', 
             capsize=3, label=r'$t_{break-up}$')
handles2, labels2 = axx.get_legend_handles_labels()
handles2 = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles2]
############################################################
############################################################

# ax.legend(handles+handles2, labels+labels2, loc='center left', columnspacing=0.6,  handletextpad=.1,
# frameon=False, ncol=1, fontsize=12, handlelength=1.5)
plt.tight_layout()
plt.savefig('chi-sf2.pdf', dpi=dpi)
plt.show()

exit()

fig, ax = plt.subplots(1,1)

def chi(oh):
    return 1/(np.sqrt(2+np.sqrt(18)*oh))

def oh(mu, gamma, rho, r):
    return mu/np.sqrt(rho*gamma*r)

x = np.linspace(3, 7, 100)
y = chi(oh(4, x, 6, R))

ax.plot(np.array(surf_tension)*72/7.45, q, 'ko', label='Simulations')
ax.plot(np.array(x)*72/7.45, y, 'k--', label=r'Theory ($\mu$, $\rho$ of pure liquid)')
ax.set_xlabel(r'$ \gamma $ [MDPD units]')
ax.set_ylabel(r'$ \chi $')
# ax.set_xlim(2,7)
ax.legend(frameon=False)

plt.show()