import pandas as pd
import numpy as np
import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.85*side, 0.55*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt
import os
from scipy import stats


R = 6
A = -50

ratio = [6, 12, 24, 48]
time = [91, 99, 94, 107]
div  = [20, 20, 20, 30]

num = []

for i, ra in enumerate(ratio):
    case = f'R{R}_ratio{ra}_A{abs(A)}'
    path = f'/home/luishcc/md-projects/analysis/cluster/break-avg/{case}/{time[i]}.csv'

    df = pd.read_csv(path)

    df.drop(df[df['size'] <= 1].index, inplace=True)
    df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
    df['radius'] = df['radius'].multiply(np.sqrt(5/3))

    main = df[df['radius'] > 5]

    num.append(main.shape[0] / div[i])

fig, ax = plt.subplots(1,1)

# ax.plot([1/i for i in ratio], num, 'ko-')
ax.plot([2*np.pi*6*i for i in ratio], num, 'ko-')

plt.show()
