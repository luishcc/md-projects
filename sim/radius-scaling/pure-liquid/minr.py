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
    for i in range(breaktime+10 ):
        # file = f'{cwd}/{dir}/surface_profile/{i}.dat'
        file = f'{dir}/surface_profile/{i}.dat'
        with open(file, 'r') as fd:
            next(fd)
            next(fd)
            data = [line.split() for line in fd]
        lst_z = [float(line[0]) for line in data]
        lst_r = [float(line[1]) for line in data]
        minR = min(lst_r)
        if minR <= 1e-5:
            break
        minZ = lst_z[lst_r.index(minR)] 
        min_r.append(minR/5.7)
        min_z.append(minZ)
    print(i, breaktime)
    z0 = (min_z[0] + min_z[1] + min_z[2] + min_z[3])*0.25
    return min_r, [abs(z-z0) for z in min_z], len(min_r)

import matplotlib.pyplot as plt
import matplotlib as mpl

dpi = 1600
side = 5
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (2.0*side, 1.0*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, (ax,ax2) = plt.subplots(1,2, sharex = False)
# fig, ax2 = plt.subplots(1,1, sharex = False)

lists = []
nn=20
# case = '/home/luishcc/hdd/radius_scaling/low-Oh'
case = '/home/luishcc/hdd/radius_scaling/high-Oh'
# case = 'high-Oh'
for i in range(nn):
    r, z, t = read_sim(f'{case}/{i+1}')
    # r, z, t = read_sim(f'{i+1}')
    lists.append(r)
    # ax.plot([t-j for j in range(t)], r, 'c--',
    #           linewidth=1, markerfacecolor='none')
    ax2.loglog([t-j for j in range(t)], r, 'c--',
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

times = [(len(mean)-j)/10 for j in range(len(mean))]
ax.plot(times, mean, 'k-', 
          markerfacecolor='none', label='Mean',
          linewidth=4)
ax.set_xlim(-10,200)          
ax.set_ylim(-0.1,1.1)          

# ax.semilogy([j/10 for j in range(len(mean))], mean, 'k-', 
#           markerfacecolor='none', label='Mean',
#           linewidth=4)

ax2.plot([len(mean)-j for j in range(len(mean))], mean, 'k-', 
          markerfacecolor='none', label='Mean',
          linewidth=4)

x0 = np.linspace(1,60,1000)
x1 = np.linspace(10,800,1000)
x2 = np.linspace(150,800,1000)

tt = np.linspace(0,200,1000)
tt2 = np.linspace(0,100,1000)

def f(t, b, c):
    return b*t**0.333 + c

def ln(t,a,b):
    return np.log(t**a)+np.log(b)
# Oh = 0.762
Oh = 0.289

times = [(len(mean)-j)/10 for j in range(len(mean))]

# yt = [i*(0.0709/Oh)/5.7**2+0.18 for i in tt]
# yt2 = [i**(2/3)/36 for i in tt2]
# yt2 = [i**(1/3)/8 for i in tt2]
yt = [i**(0.42)/9 for i in tt]
yt2 = [i**(0.666)/20 for i in tt]
# yt3 = [i*(0.0709/Oh)/100+0.57 for i in tt]
# yt3 = [i*(0.0304/Oh)/10+0.1 for i in tt]
yt3 = [i**0.55/18 for i in tt]
# yt4 = [np.exp(-(i-len(mean)/10)*0.315) for i in tt]

def power(t,a,b):
    return a*t**b
from scipy.optimize import curve_fit
# pars, cov = curve_fit(f=power, xdata=np.array(times[20:-50]), ydata=mean[20:-50], p0=[1/18,0.55], bounds=(-np.inf, np.inf))
pars, cov = curve_fit(f=ln, xdata=np.array(times[20:-50]), ydata=mean[20:-50], p0=[1/18,0.55], bounds=(-np.inf, np.inf))

print(pars)

# ytt = power(tt, *pars)
ytt = ln(tt, *pars)

ax.plot(tt,yt, 'b--', linewidth=3, label=r'$(t_b-t)^{0.42}$')
ax.plot(tt,yt2, 'g--', linewidth=3, label=r'$(t_b-t)^{1/3}$')
ax.plot(tt,yt3, 'y--', linewidth=3, label=r'$(t_b-t){0.0709/Oh}$')
ax.plot(tt,ytt, 'c--', linewidth=3, label=r'$(t/$')

ax.legend()

# y0 = [i**0.1/10 for i in x0]
y0 = [0.09*np.exp(i*0.013) for i in x0]
# y0 = [i**0.333/25 for i in x0]
# y1 = [i**0.47/45 for i in x1]
y1 = [i**0.55/50 for i in x1]
# y1 = [i**0.5/38 for i in x1]
y2 = [(i**.666)/110 for i in x2]

ax2.plot(x0,y0, 'y--', linewidth=3, label=r'$(t_b-t)^{0.1}$')
ax2.plot(x1,y1, 'g--', linewidth=3, label=r'$(t_b-t)^{0.48}$')
ax2.plot(x2,y2, 'b--', linewidth=3, label=r'$(t_b-t)^{0.61}$')

# ax.errorbar([i for i in range(len(mean))], mean, yerr=variance**(1/2))

ax2.set_ylabel(r'$h_{{min}}/R_0$')
ax2.set_xlabel(r'$(t_b-t)$')
# ax.set_ylim(0,1)
# ax.set_xlim(0,80)
#  ax.set_xlabel(r'$t$')
ax2.legend(frameon=False)

plt.tight_layout()
# plt.savefig(f'low.pdf', dpi=dpi)
# plt.savefig(f'high.pdf', dpi=dpi)

# plt.show()

# from scipy.signal import savgol_filter

# plt.figure()

# # mean2 = savgol_filter( mean, 100, 5)
# mean2 = mean

# dy = np.gradient(np.log(mean2), np.log(times), edge_order=2)
# w = savgol_filter( dy, 100, 3)

# plt.semilogx(times, dy)
# plt.plot(times, w)

# plt.ylim(-0.2,0.8)

plt.show()
