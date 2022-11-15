import os
import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix

import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.4*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


dir = '/home/luishcc/md-projects/analysis/satellite/csv_80/axis'
# dir = os.getcwd()

# nam = ['cooz-48000.csv', 'cooz-44000.csv', 'cooz-38000.csv' ]
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

fig, ax = plt.subplots(1,1)

n = len(lst[0])
x = np.linspace(-0.5,0.5,n)

ax.plot(x, lst[1], 'k-', label=r'$t_3$')
ax.plot(x, lst[0], 'g-.', label=r'$t_2$')
ax.plot(x, lst[2], 'b--', label=r'$t_1$')

ax.legend(loc='lower right')
ax.set_xlabel(r'$x/L$')
ax.set_ylabel(r'$v_z$')
# ax.tick_params(axis='x', which='both', bottom=False,
#                 top=False, labelbottom=False)

plt.savefig('80.png', bbox_inches='tight', dpi=dpi )


plt.show()
