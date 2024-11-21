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
    
amp = np.array([1,3,5,10,15,20,25])
ndrops = np.array([1,2,4,8,12,16])

fig, ax = plt.subplots(1,1)

colors = [ 'indigo', 'black', 'blue', 'green', 'brown','gray']
markers = [ 'p', 'o', '^', 's', 'd', 'x']
linestyles = ['-', '--', '-.', '--','--', '-.']
iniang = [r'$47^{\circ}$', r'$75^{\circ}$', r'$100^{\circ}$', r'$120^{\circ}$' ]
iniang = [2,4,6,8]

results = np.zeros((len(amp), len(ndrops)))
stds = np.zeros((len(amp), len(ndrops)))
for i, a in enumerate(amp):
    for j, nd in enumerate(ndrops):
        temp_res = []
        for k in range(10):
            file = f'{a:.0f}/{nd:.0f}/{k+1:.0f}/{filename}'
            # print(file)
            if not os.path.isfile(file):
                continue
            with open(file, 'r') as fd:
                temp_res.append(float(fd.readline().split()[0]))
        temp_res = np.array(temp_res)
        results[i,j] = temp_res.mean()
        stds[i,j] = temp_res.std()

free = []
for k in range(10):
    file = f'0/free/{k+1:.0f}/{filename}'
    if not os.path.isfile(file):
        continue
    with open(file, 'r') as fd:
        free.append(float(fd.readline().split()[0]))
free = np.array(free)

uniform = []
uniform_std = []
h0 = [1,3,5,10]
for i in h0:
    temp = []
    for k in range(5):
        file = f'type2/{i}/{k+1:.0f}/{filename}'
        if not os.path.isfile(file):
            continue
        with open(file, 'r') as fd:
            temp.append(float(fd.readline().split()[0]))
    uniform.append(np.mean(temp))
    uniform_std.append(np.std(temp))

for i, nd in enumerate(ndrops):
    # print(i)
    color = colors[i]
    marker = markers[i]
    style = linestyles[i]
	
    ax.plot(amp, results[:,i], color=color,
            linestyle=style, linewidth=1.2,
            label=rf'${nd:.0f}$',  markersize=6,
            markeredgewidth=1, marker=marker, 
            markerfacecolor='none')
    # ax.plot(amp, results[:,i], color=color, markersize=6,
    #         linestyle='none', markeredgewidth=1,
    #         marker=marker, markerfacecolor='none')
    ax.errorbar(amp, results[:,i], yerr=stds[:,i],
            linestyle='none', ecolor = color, 
            color=color, capsize= 2, capthick=1)


# ax.errorbar(h0, uniform, yerr=uniform_std,
#             linestyle='--', ecolor ='black', 
#             marker='P',
#             color='black', capsize= 2, capthick=1)


ax.plot([0,50], [free.mean()]*2, 'r-', linewidth=1.2)
ax.fill_between([0,50], [free.mean()-free.std()]*2, 
                [free.mean()+free.std()]*2, color='red', alpha = 0.2)

ax.set_ylabel(r'$t_{break}$')
ax.set_xlabel(r'$H_0$')
# ax.set_ylim(5,60)
ax.set_xlim(0,26)

ax.annotate(r'Natural breakup', xy=(12, 96), xytext=(10, 125), fontsize=10, 
            arrowprops=dict(facecolor='black', mutation_scale=20,
                            headlength=8, headwidth=4,
                            width=.8))

handles, labels = ax.get_legend_handles_labels()

han1 = [handles[i] for i in range(6)]
lab1 = [labels[i] for i in range(6)]

legend1 = plt.legend(han1, lab1, frameon=False, 
      loc='upper right', ncol=2, handlelength=0,
      title=r'$N_{d}$', title_fontsize=11,
      columnspacing=1,
      fontsize=11)
# ax.grid(True)

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
# fig.savefig(f'{savename}.png', dpi=dpi, transparent=True)
fig.savefig(f'{savename}.pdf', dpi=dpi)
# plt.show()        

