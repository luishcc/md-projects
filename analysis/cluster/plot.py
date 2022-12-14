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

fig, ax0 = plt.subplots(ncols=1, nrows=1)


import pandas as pd

R = 4
ratio = 48
A = -50

snap = 86

file = f'~/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'
# file = f'~/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'

df = pd.read_csv(file)
df.drop(df[df['size'] <= 2].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
df['radius'] = df['radius'].multiply(np.sqrt(5/3))
df['radius'].plot.hist(bins=100, alpha=0.4, ax=ax0, density=True, color='b')
df['radius'].plot.kde(bw_method=0.1, ax=ax0, color='k')
# ax0.set_xlim(0,16)
ax0.set_xlabel('$R_D$')
ax0.set_ylabel('Distribution Density')
# ax0.annotate('', xy=(3.7, 0.165), xytext=(1.9,0.14),
#             arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
#             )
# ax0.annotate('', xy=(6.4,0.292), xytext=(8.76,0.26),
#             arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
#             )
# ax0.annotate('Main Droplets', xy=(3.5, 0.3))
# ax0.annotate('Satellite Droplets', xy=(3, 0.17))

# plt.savefig(f'dis.png', transparent=True, dpi=1600)


plt.show()
