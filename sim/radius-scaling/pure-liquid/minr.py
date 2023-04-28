import os
import numpy as np

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

def read_sim(dir):
    cwd = os.getcwd()
    min_r = []
    min_z = []
    breaktime = get_breaktime(dir)
    for i in range(breaktime):
        file = f'{cwd}/{dir}/surface_profile/{i}.dat'
        with open(file, 'r') as fd:
            next(fd)
            next(fd)
            data = [line.split() for line in fd]
        lst_z = [float(line[0]) for line in data]
        lst_r = [float(line[1]) for line in data]
        minR = min(lst_r)
        if minR <= 1e-4:
            break
        minZ = lst_z[lst_r.index(minR)] 
        min_r.append(minR)
        min_z.append(minZ)
    z0 = (min_z[0] + min_z[1] + min_z[2] + min_z[3])*0.25
    return min_r, [abs(z-z0) for z in min_z], len(min_r)

import matplotlib.pyplot as plt
import matplotlib as mpl

dpi = 1600
side = 5
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (1.8*side, 1.0*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, (ax) = plt.subplots(1,1, sharex = False)

lists = []
for i in range(10):
    r, z, t = read_sim(i+1)
    lists.append(r)
    ax.loglog([t-j for j in range(t)], r, 'c--',
              linewidth=1, markerfacecolor='none')
    # ax2.plot([j for j in range(t)], z, markerfacecolor='none', label=i)

mean = []
for i in range(max([len(l) for l in lists])):
    temp = []
    for lst in lists:
        if len(lst) > i:
            temp.append(lst[-i-1])
    mean.append(sum(temp)/len(temp))
mean.reverse()

ax.plot([len(mean)-j for j in range(len(mean))], mean, 'k-', 
          markerfacecolor='none', label='Mean',
          linewidth=4)

x0 = np.linspace(1,30,1000)
x1 = np.linspace(15,200,1000)
x2 = np.linspace(100,900,1000)

y0 = [i**0.1/2 for i in x0]
y1 = [i**0.418/6 for i in x1]
y2 = [(i**.6666)/19.5 for i in x2]

ax.plot(x0,y0, 'y--', linewidth=5, label=r'$(t_b-t)^{0.xx}$')
ax.plot(x1,y1, 'g--', linewidth=5, label=r'$(t_b-t)^{0.418}$')
ax.plot(x2,y2, 'b--', linewidth=5, label=r'$(t_b-t)^{2/3}$')

# ax.errorbar([i for i in range(len(mean))], mean, yerr=variance**(1/2))

ax.set_ylabel(r'$h_{{min}}$')
ax.set_xlabel(r'$(t_b-t)^*$')
# ax.set_xlabel(r'$t$')
ax.legend(frameon=False)

plt.tight_layout()
# plt.savefig(f'time.pdf', dpi=dpi)

plt.show()