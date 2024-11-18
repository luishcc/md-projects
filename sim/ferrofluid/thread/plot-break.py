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


filename = 'breaktime.txt'
    
amp = np.array([5,10,15,20,25])
ndrops = np.array([2,4,8,16])



fig, ax = plt.subplots(1,1)

colors = ['black', 'blue', 'green', 'gray']
markers = ['o', '^', 's', 'x']
linestyles = ['-', '--', '-.', '--']
iniang = [r'$47^{\circ}$', r'$75^{\circ}$', r'$100^{\circ}$', r'$120^{\circ}$' ]
iniang = [2,4,6,8]

results = np.zeros((len(amp), len(ndrops)))
stds = np.zeros((len(amp), len(ndrops)))
for i, a in enumerate(amp):
    for j, nd in enumerate(ndrops):
        temp_res = []
        for k in range(10):
            file = f'{a:.0f}/{nd:.0f}/{k+1:.0f}/{filename}'
            print(file)
            if not os.path.isfile(file):
                continue
            with open(file, 'r') as fd:
                temp_res.append(float(fd.readline().split()[0]))
        temp_res = np.array(temp_res)
        results[i,j] = temp_res.mean()
        stds[i,j] = temp_res.std()


for i, nd in enumerate(ndrops):
    print(i)
    color = colors[i]
    marker = markers[i]
    style = linestyles[i]
	
    ax.plot(amp, results[:,i], color=color,
            linestyle=style, linewidth=1.2,
            label=rf'${nd:.0f}$')
    ax.plot(amp, results[:,i], color=color, markersize=6,
            linestyle='none', markeredgewidth=1,
            marker=marker, markerfacecolor='none')
    ax.errorbar(amp, results[:,i], yerr=stds[:,i],
            linestyle='none', ecolor = color, 
            color=color, capsize= 2, capthick=1)


ax.set_ylabel(r'$t_{break}$')
ax.set_xlabel(r'$H_0$')
# ax.set_ylim(5,20)

handles, labels = ax.get_legend_handles_labels()

han1 = [handles[i] for i in range(4)]
lab1 = [labels[i] for i in range(4)]

legend1 = plt.legend(han1, lab1, frameon=False, 
      loc='upper right', ncol=2, handlelength=1.7,
      title=r'$N_{drops}$', title_fontsize=11,
      columnspacing=1.2,
      fontsize=11)
ax.grid(True)

# han2 = [handles[i*8] for i in range(3)]
# lab2 = [labels[i*8] for i in range(3)]

# legend2 = plt.legend(han2, lab2, frameon=False, loc='upper left',
#       title='Concentration', title_fontsize=11, 
#       handlelength=1.7, ncol=2, columnspacing=1.2,
#       fontsize=11)

ax.add_artist(legend1)
# ax.add_artist(legend2)

savename = filename.split('.')[0]
fig.tight_layout()
fig.savefig(f'{savename}.pdf', dpi=dpi)
# plt.show()        

