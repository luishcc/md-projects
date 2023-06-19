import os
import numpy as np

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

def read_sim(dir):
    # cwd = os.getcwd()
    min_r = []
    min_z = []
    breaktime = get_breaktime(dir)
    for i in range(breaktime+5):
        # file = f'{cwd}/{dir}/surface_profile/{i}.dat'
        file = f'{dir}/surface_profile/{i}.dat'
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
        min_r.append(minR/8.1)
        min_z.append(minZ)
    z0 = (min_z[0] + min_z[1] + min_z[2] + min_z[3])*0.25
    print(i, breaktime, i-breaktime)
    return min_r, [abs(z-z0) for z in min_z], len(min_r)

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

lists = []

nn=20

case = '/home/luishcc/hdd/radius_scaling/surfactant/0.5'
# case = '/home/luishcc/hdd/radius_scaling/surfactant/2.3'
# case = '/home/luishcc/hdd/radius_scaling/low-Oh'
# case = '/home/luishcc/hdd/radius_scaling/high-Oh'
# case = 'high-Oh'
for i in range(nn):
    if i <0 or i>29 or i==-1:
        continue
    r, z, t = read_sim(f'{case}/{i+1}')
    # r, z, t = read_sim(f'{i+1}')
    lists.append(r)
    # ax.plot([t-j for j in range(t)], r, 'c--',
    #           linewidth=1, markerfacecolor='none')
    # ax2.loglog([t-j for j in range(t)], r, 'c--',
    #           linewidth=1, markerfacecolor='none')
    ax2.loglog([t-j for j in range(t)], r, 
            linewidth=1, markerfacecolor='none')
    # ax2.plot([j for j in range(t)], z, markerfacecolor='none', label=i)

ax2.legend()
mean = []
for i in range(max([len(l) for l in lists])):
    temp = []
    for lst in lists:
        if len(lst) > i:
            temp.append(lst[-i-1])
    mean.append(sum(temp)/len(temp))
mean.reverse()

# ax.plot([(len(mean)-j)/10 for j in range(len(mean))], mean, 'k-', 
#           markerfacecolor='none', label='Mean',
#           linewidth=4)

# ax.plot([j/10 for j in range(len(mean))], mean, 'k-', 
#           markerfacecolor='none', label='Mean',
#           linewidth=4)

ax2.plot([len(mean)-j for j in range(len(mean))], mean, 'k-', 
          markerfacecolor='none', label='Mean',
          linewidth=4)

x0 = np.linspace(1,8,1000)
x1 = np.linspace(20,600,1000)
x2 = np.linspace(150,600,1000)
x3 = np.linspace(5,20,1000)

tt = np.linspace(0,80,1000)
tt2 = np.linspace(0,100,1000)

def f(t, b, c):
    return b*t**0.333 + c

Oh = 0.762
# Oh = 0.289

times = [(len(mean)-j)/10 for j in range(len(mean))]

yt = [i*(0.0709/Oh)/5.7**2+0.18 for i in tt]
yt2 = [i**(2/3)/36 for i in tt2]
yt2 = [i**(1/3)/8 for i in tt2]
# yt = [i**(0.42)/8 for i in tt]
# yt2 = [i**(0.666)/24 for i in tt]

# from scipy.optimize import curve_fit
# pars, cov = curve_fit(f=f, xdata=np.array(times), ydata=mean, p0=[0.2,0.1], bounds=(-np.inf, np.inf))

# tt2=np.array(times)
# yt2 = f(tt2, *pars)

# ax.plot(tt,yt, 'b--', linewidth=5, label=r'$(t_b-t){0.0709/Oh}$')
# ax.plot(tt2,yt2, 'g--', linewidth=5, label=r'$(t_b-t)^{1/3}$')

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

# ax.errorbar([i for i in range(len(mean))], mean, yerr=variance**(1/2))

ax2.set_ylabel(r'$h_{{min}}/R_0$')
ax2.set_xlabel(r'$(t_b-t)$')
# ax.set_ylim(0,1)
# ax.set_xlim(0,80)
#  ax.set_xlabel(r'$t$')
ax2.legend(frameon=False)

plt.tight_layout()
# plt.savefig(f'surfactant-1.6.pdf', dpi=dpi)
# plt.savefig(f'surfactant-2.3.pdf', dpi=dpi)

# plt.show()

from scipy.signal import savgol_filter

plt.figure()

# mean2 = savgol_filter( mean, 100, 5)
mean2 = mean

dy = np.gradient(np.log(mean2), np.log(times), edge_order=2)
w = savgol_filter( dy, 50, 4)

plt.semilogx(times, dy)
plt.plot(times, w)

plt.ylim(-0.2,0.8)

plt.show()
