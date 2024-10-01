import numpy as np
import os

import matplotlib as mpl

import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (1.7*side, 1.*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
from matplotlib import container




fig, axs = plt.subplots(ncols=2, nrows=2)


fig.subplots_adjust(wspace=.25)
fig.subplots_adjust(hspace=.4)

fig.tight_layout()

ax2 = axs[0,0]
ax0 = axs[0,1]

ax11 = axs[1,0]
ax12 = axs[1,1]


import pandas as pd

R = 2
ratio = 48
A = -40
snap = 30

# file = f'~/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'
file = f'~/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'

df = pd.read_csv(file)
df.drop(df[df['size'] <= 3].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
df['radius'] = df['radius'].multiply(np.sqrt(5/3))
df['radius'].plot.hist(bins=70, alpha=0.4, ax=ax0, density=True, color='b')
df['radius'].plot.kde(bw_method=0.25, ax=ax0, color='k')
ax0.set_xlim(0,6.2)
ax0.set_ylim(0,1.2)
ax0.set_xlabel('$R_D$')
ax0.set_ylabel('Distribution Density')
ax0.annotate('', xy=(1.3, 0.4), xytext=(1.1,0.1),
            arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
            )
ax0.annotate('', xy=(2.,0.9), xytext=(3.,0.7),
            arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
            )
ax0.annotate('Main Droplets', xy=(1.0, 1.))
ax0.annotate('Satellite Droplets', xy=(0.5, 0.45))

##########################################

path = f'/home/luishcc/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}/'

separation = 2


num_cluster = {}
num_main = {}
num_satellite = {}
num_drops = {}

num_cluster2 = {}
num_main2 = {}
num_satellite2 = {}
num_drops2 = {}
for file in os.scandir(path):

    try:
        df = pd.read_csv(file.path)
    except:
        continue
    name = int(file.name.split('.')[0])

    print(df.shape)


    df.drop(df[df['size'] <= 1].index, inplace=True)
    # df.drop(df[df['radius'] > 5].index, inplace=True)
    # df.drop(df[df['size'] > 1000].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
    # df.drop(df[df['asphericity'] > 3].index, inplace=True)
    df['radius'] = df['radius'].multiply(np.sqrt(5/3))


    satellite = df[df['radius'] < separation]
    main = df[df['radius'] > separation]
    #
    # satellite = satellite.multiply(1/(30*1810))
    # main = main.multiply(1/(30*1810))

    print(df.shape)
    # num_cluster[name] = df.shape[0] / (30 * 1810)
    # num_drops[name] = df.shape[0]  / (30 * 1810)
    # num_main[name] = main.shape[0] / (30 * 1810)
    # num_satellite[name] = satellite.shape[0] / (30 * 1810)

    num_cluster[name] = df.shape[0] / (30 * 2*np.pi*1.55)
    num_drops[name] = df.shape[0]  / (30 * 2*np.pi*1.55)
    num_main[name] = main.shape[0] / (30 * 2*np.pi*1.55)
    num_satellite[name] = satellite.shape[0] / (30 * 2*np.pi*1.55)

    num_cluster2[name] = df.shape[0]
    num_drops2[name] = df.shape[0]
    num_main2[name] = main.shape[0]
    num_satellite2[name] = satellite.shape[0]
    print()


list1 = sorted(num_cluster.items())
list2 = sorted(num_drops.items())
list3 = sorted(num_satellite.items())
list4 = sorted(num_main.items())

x1, y1 = zip(*list1)
x2, y2 = zip(*list2)
x3, y3 = zip(*list3)
x4, y4 = zip(*list4)

x = np.linspace(int(x1[0]), int(x1[-1]), len(y2))

max_snap1 = max(num_cluster, key=num_cluster.get)
max_snap2 = max(num_drops, key=num_drops.get)
max_snap3 = max(num_satellite, key=num_satellite.get)
max_snap4 = max(num_main, key=num_main.get)

ax2.set_ylabel(r'$\langle N_{droplets} \rangle /2\pi R_0$')
ax2.set_xlabel(r'$t-t_b$')

ax2.set_ylim(0,1.6)
ax2.annotate(r'$A=-40$, $R_0=2$', xy=(25., 0.5))
ax2.set_xlim(0,60)
# plt.plot(x, y2, 'k-', label=r'Total, $\kappa^2 < 0.2$')
# plt.plot(x, y3, 'k--', label=r'Satellite, $\kappa^2 < 0.2$')
# plt.plot(x, y4, 'b-.', label=r'Main, $\kappa^2 < 0.2$')

ax2.plot(x, y2, 'k-', label=r'Total')
ax2.plot(x, y3, 'k--', label=r'Satellite')
ax2.plot(x, y4, 'b-.', label=r'Main')

ax2.scatter(max_snap2, num_drops[max_snap2], color='k')


# ax2.scatter(max_snap3, num_satellite[max_snap3], color='k')
# ax2.scatter(max_snap4, num_main[max_snap4], color='k')
# plt.grid(True)
# plt.legend(loc='upper left', prop={'size': 11.})
ax2.legend(loc=('upper left'), frameon=False)


###################################
R = 2
ratio = 48
A = -90
snap = 40

# file = f'~/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'
file = f'~/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'

df = pd.read_csv(file)
df.drop(df[df['size'] <= 3].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
df['radius'] = df['radius'].multiply(np.sqrt(5/3))
df['radius'].plot.hist(bins=70, alpha=0.4, ax=ax12, density=True, color='b')
df['radius'].plot.kde(bw_method=0.3, ax=ax12, color='k')
ax12.set_xlim(0,6.2)
ax12.set_ylim(0,1.2)
ax12.set_xlabel('$R_D$')
ax12.set_ylabel('Distribution Density')
ax12.annotate('', xy=(1.3, 0.35), xytext=(1.1,0.1),
            arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
            )
ax12.annotate('', xy=(2.5,0.7), xytext=(3.5,0.5),
            arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
            )
ax12.annotate('Main Droplets', xy=(2., 0.75))
ax12.annotate('Satellite Droplets', xy=(0.5, 0.4))

##########################################

path = f'/home/luishcc/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}/'

separation = 2

num_cluster = {}
num_main = {}
num_satellite = {}
num_drops = {}

for file in os.scandir(path):

    try:
        df = pd.read_csv(file.path)
    except:
        continue
    name = int(file.name.split('.')[0])

    df.drop(df[df['size'] <= 1].index, inplace=True)
    # df.drop(df[df['radius'] > 5].index, inplace=True)
    # df.drop(df[df['size'] > 1000].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
    # df.drop(df[df['asphericity'] > 3].index, inplace=True)
    df['radius'] = df['radius'].multiply(np.sqrt(5/3))

    satellite = df[df['radius'] < separation]
    main = df[df['radius'] > separation]

    print(df.shape)
    num_cluster[name] = df.shape[0] / (30 * 2*np.pi*1.3)
    num_drops[name] = df.shape[0]  / (30 * 2*np.pi*1.3)
    num_main[name] = main.shape[0] / (30 * 2*np.pi*1.3)
    num_satellite[name] = satellite.shape[0] / (30 * 2*np.pi*1.3)


list1 = sorted(num_cluster.items())
list2 = sorted(num_drops.items())
list3 = sorted(num_satellite.items())
list4 = sorted(num_main.items())

x1, y1 = zip(*list1)
x2, y2 = zip(*list2)
x3, y3 = zip(*list3)
x4, y4 = zip(*list4)

x = np.linspace(int(x1[0]), int(x1[-1]), len(y2))

max_snap2 = max(num_drops, key=num_drops.get)

ax11.set_ylabel(r'$\langle N_{droplets} \rangle /2\pi R_0$')
ax11.set_xlabel(r'$t-t_b$')
ax11.set_ylim(0,1.6)
ax11.set_xlim(0,60)
ax11.plot(x, y2, 'k-', label=r'Total')
ax11.plot(x, y3, 'k--', label=r'Satellite')
ax11.plot(x, y4, 'b-.', label=r'Main')
ax11.scatter(max_snap2, num_drops[max_snap2], color='k')
ax11.annotate(r'$A=-90$, $R_0=2$', xy=(25., 1.))
ax11.legend(loc=('upper left'), frameon=False)

from matplotlib.transforms import ScaledTranslation
ax2.text(
         0.0, 1.0, 'a)', transform=(
            ax2.transAxes + ScaledTranslation(-50/72, -20/72, fig.dpi_scale_trans)),
        fontsize=24, va='bottom', fontfamily='serif')
ax11.text(
         0.0, 1.0, 'b)', transform=(
            ax11.transAxes + ScaledTranslation(-50/72, -20/72, fig.dpi_scale_trans)),
        fontsize=24, va='bottom', fontfamily='serif')

plt.savefig('ch3cluster2.pdf', bbox_inches='tight', dpi=dpi )

# plt.show()
