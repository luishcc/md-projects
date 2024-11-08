import os
import sys
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


filename = 'area.txt'
    

cons = np.linspace(0.05, 0.15, int((0.15-0.05)/0.05+1))
walls = np.linspace(2, 8, int((8-2)/2+1))
dips = np.linspace(0, 3, int(3/0.25+1))

fig, ax = plt.subplots(1,1)


colors = ['black', 'blue', 'green']
markers = ['o', '^', 's', 'x']
linestyles = ['-', '--', '-.']
iniang = [r'$47^{\circ}$', r'$75^{\circ}$', r'$100^{\circ}$', r'$120^{\circ}$' ]
iniang = [2,4,6,8]


import random
for i, con in enumerate(cons):
    color = colors[i]
    for j, wall in enumerate(walls):
        height = []
        std = []
        marker = markers[j]
        style = linestyles[i]
        for dip in dips:
            file = f'{con:.2f}/{wall:.0f}/{dip:.2f}/{filename}'
            print(file)
            if not os.path.isfile(file):
             #   line.append(random.randrange(20, 120, 3))
                continue
            with open(file, 'r') as fd:
                height.append(float(fd.readline().split()[0]))
                std.append(float(fd.readline().split()[0]))
	
        ax.plot(dips[:len(height)], height, color=color,
                linestyle=style, linewidth=1.2,
                label=rf'${con*100:.0f}\%$')
        ax.plot(dips[:len(height)], height, color=color, markersize=6,
                linestyle='none', markeredgewidth=1,
                marker=marker, markerfacecolor='none',
                label=iniang[j])
        # ax.errorbar(dips[:len(height)], height, yerr=std,
        #         linestyle='none')

ax.set_ylabel(r'$A$ [$r_c^2$]')
ax.set_xlabel(r'$\mu$')
ax.set_ylim(20,110)

handles, labels = ax.get_legend_handles_labels()

han1 = [handles[i*2+1] for i in range(4)]
lab1 = [labels[i*2+1] for i in range(4)]

legend1 = plt.legend(han1, lab1, frameon=False, 
      loc='upper right', ncol=2, handlelength=0,
      title=r'$\epsilon_{wall}$', title_fontsize=11,
      columnspacing=1.2,
      fontsize=11)
ax.grid(True)

han2 = [handles[i*8] for i in range(3)]
lab2 = [labels[i*8] for i in range(3)]

legend2 = plt.legend(han2, lab2, frameon=False, loc='upper left',
      title='Concentration', title_fontsize=11, 
      handlelength=1.7, ncol=2, columnspacing=1.2,
      fontsize=11)

ax.add_artist(legend1)
ax.add_artist(legend2)

savename = filename.split('.')[0]
fig.tight_layout()
fig.savefig(f'{savename}.pdf', dpi=dpi)
#plt.show()        

