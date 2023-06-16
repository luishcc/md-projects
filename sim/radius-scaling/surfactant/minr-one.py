import os
import numpy as np

with open(f'1/breaktime.txt', 'r') as fd:
    breaktime = int(fd.readline())

cwd = os.getcwd()
min_r = []
min_z = []
for i in range(breaktime-2):
    file = f'1/surface_profile/{i}.dat'
    try:
        with open(file, 'r') as fd:
            next(fd)
            next(fd)
            data = [line.split() for line in fd]
    except:
        continue
    lst_z = [float(line[0]) for line in data]
    lst_r = [float(line[1]) for line in data]
    minR = min(lst_r)
    if minR <= 1e-4:
        break
    minZ = lst_z[lst_r.index(minR)] 
    min_r.append(minR/8.1)
    min_z.append(minZ)
    print(i)
    print(minR)
z0 = (min_z[0] + min_z[1] + min_z[2] + min_z[3])*0.25

import matplotlib.pyplot as plt
import matplotlib as mpl

dpi = 1600
side = 5
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (1.0*side, 1.0*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

# fig, (ax,ax2) = plt.subplots(1,2, sharex = False)
fig, ax2 = plt.subplots(1,1, sharex = False)


x0 = np.linspace(1,8,1000)
x1 = np.linspace(20,600,1000)
x2 = np.linspace(150,600,1000)
x3 = np.linspace(5,20,1000)

times = [len(min_r)-j for j in range(len(min_r))]
ax2.loglog(times, min_r)

y0 = [i**0.1/7 for i in x0]
# y0 = [i**0.333/25 for i in x0]
y1 = [i**0.42/13 for i in x1]
# y1 = [i**0.5/38 for i in x1]
y2 = [(i**.666)/90 for i in x2]
y3 = [(i**.333)/15 for i in x3]

ax2.plot(x0,y0, 'y--', linewidth=5, label=r'$(t_b-t)^{0.1}$')
ax2.plot(x1,y1, 'g--', linewidth=5, label=r'$(t_b-t)^{0.42}$')
# ax2.plot(x2,y2, 'b--', linewidth=5, label=r'$(t_b-t)^{0.666}$')
# ax2.plot(x3,y3, 'r--', linewidth=5, label=r'$(t_b-t)^{0.333}$')

ax2.set_ylabel(r'$h_{{min}}/R_0$')
ax2.set_xlabel(r'$(t_b-t)$')
# ax.set_ylim(0,1)
# ax.set_xlim(0,80)
#  ax.set_xlabel(r'$t$')
ax2.legend(frameon=False)

plt.tight_layout()

plt.show()
