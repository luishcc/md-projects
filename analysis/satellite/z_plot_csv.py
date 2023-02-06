import os
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix

import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12*2,
    'figure.figsize': (0.8*side, 0.8*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


dir = '/home/luishcc/md-projects/analysis/satellite/csv_80/axis'
# dir = os.getcwd()

# nam = ['cooz-48000.csv', 'cooz-44000.csv', 'cooz-38000.csv' ] # A=50
nam = ['cooz-53200.csv', 'cooz-49200.csv', 'cooz-40000.csv' ]

lst = []
lst_label = []
for file in os.scandir(dir):
    if file.name not in nam:
        continue

    label = file.name.split('.')[0]
    label = label.split('-')[1]
    lst_label.append(label)

    df = pd.read_csv(file, header=None)
    df = df.transpose()

    lst.append(df[1].tolist())


fig, (ax, ax2) = plt.subplots(2,1, sharex=True)
fig.subplots_adjust(hspace=0.05)

n = len(lst[0])
x = np.linspace(-0.5,0.5,n)

ax.plot(x, lst[1], 'k-', label=r'$t_3$')
ax.plot(x, lst[0], 'g-.', label=r'$t_2$')
ax.plot(x, lst[2], 'b--', label=r'$t_1$')

from numpy import diff
from scipy import signal
ddy = signal.savgol_filter(lst[1], 30, 4)
# ddy = np.array(lst[1])
deriv = diff(ddy)
deriv = deriv/max(deriv)
# deriv = signal.savgol_filter(deriv, 20, 4)

ddy2 = signal.savgol_filter(lst[0], 30, 4)
# ddy2 = np.array(lst[0])
deriv2 = diff(ddy2)
deriv2 = deriv2/max(deriv2)
# deriv2 = signal.savgol_filter(deriv2, 20, 4)

ddy3 = signal.savgol_filter(lst[2], 30, 4)
# ddy3 = np.array(lst[2])
deriv3 = diff(ddy3)
deriv3 = deriv3/max(deriv3)
# deriv3 = signal.savgol_filter(deriv3, 20, 4)


ax2.plot(np.linspace(-0.5,0.5, len(deriv)), (deriv), 'k-', label=r'$t_3$')
ax2.plot(np.linspace(-0.5,0.5, len(deriv2)), (deriv2), 'g-.', label=r'$t_2$')
ax2.plot(np.linspace(-0.5,0.5, len(deriv3   )), (deriv3), 'b--', label=r'$t_1$')
ax2.set_ylabel(r'$\partial v_z/\partial z$')

# ax2.plot(np.linspace(-0.5,0.5, len(ddy)), (ddy/max(ddy)))
ax2.set_ylim(-1.1,1.1)




ax.legend(loc='upper left', ncol=3, handlelength=.8, borderaxespad=0.2,
        columnspacing=0.6, fontsize=20, frameon=False)
# ax2.legend(loc='lower center', ncol=3, handlelength=.8, borderaxespad=0.2,
#         columnspacing=0.6, fontsize=20, frameon=False)
ax2.set_xlabel(r'$z/L$')
ax.set_ylabel(r'$v_z$')
ax.annotate(r'$Oh=0.461 $', xy=(0.07, -0.6))
# ax.annotate(r'$Oh=0.174 $', xy=(0.05, -0.5))
ax.set_ylim(-1.1,1.1)
# ax.set_ylim(-0.7,0.7)
# ax.tick_params(axis='x', which='both', bottom=False,
#                 top=False, labelbottom=False)

plt.savefig('80.pdf', bbox_inches='tight', dpi=2*dpi )


plt.show()
