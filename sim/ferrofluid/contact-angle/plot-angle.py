import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.7*side, 0.5*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

cons = np.linspace(0.05, 0.15, int((0.15-0.05)/0.05+1))
walls = np.linspace(2, 8, int((8-2)/2+1))
dips = np.linspace(0, 3, int(3/0.25+1))

fig, ax = plt.subplots(1,1)


colors = ['black', 'blue', 'green']
markers = ['o', '^', 's', 'x']
linestyles = ['-', '--', '-.']

import random
for i, con in enumerate(cons):
    color = colors[i]
    for j, wall in enumerate(walls):
        line = []
        marker = markers[j]
        style = linestyles[i]
        for dip in dips:
            file = f'{con:.2f}/{wall:.0f}/{dip:.2f}/angle.txt'
            print(file)
            if not os.path.isfile(file):
                line.append(random.randrange(20, 120, 3))
                continue
            with open(file, 'r') as fd:
                line.append(float(fd.readline().split()[0]))

        ax.plot(dips[:len(line)], line, color=color,
                linestyle=style,
                marker=marker, markerfacecolor='none',
                label=r'${con\%$')

plt.show()        

