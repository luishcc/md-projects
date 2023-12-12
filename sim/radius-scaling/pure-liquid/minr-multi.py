import os
import numpy as np

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

def read_sim(dir,r0):
    # cwd = os.getcwd()
    min_r = []
    min_z = []
    breaktime = get_breaktime(dir)
    for i in range(breaktime):
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
        min_r.append(minR/r0)
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

fig, ax2 = plt.subplots(1,1)

lists = []
nn=20
case = '/home/luishcc/hdd/radius_scaling/high-Oh'
for i in range(nn):
    r, z, t = read_sim(f'{case}/{i+1}', 5.7)
    # r, z, t = read_sim(f'{i+1}')
    lists.append(r)

mean = []
for i in range(max([len(l) for l in lists])):
    temp = []
    for lst in lists:
        if len(lst) > i:
            temp.append(lst[-i-1])
    mean.append(sum(temp)/len(temp))
mean.reverse()



lists2 = []
nn=20
case = '/home/luishcc/hdd/radius_scaling/low-Oh'
for i in range(nn):
    r, z, t = read_sim(f'{case}/{i+1}', 5.6)
    lists2.append(r)

mean2 = []
for i in range(max([len(l) for l in lists2])):
    temp = []
    for lst in lists2:
        if len(lst) > i:
            temp.append(lst[-i-1])
    mean2.append(sum(temp)/len(temp))
mean2.reverse()

# mean.append(0)
# mean2.append(0)



times = [(len(mean)-j)/10 for j in range(len(mean))]
times2 = [(len(mean2)-j)/10 for j in range(len(mean2))]



def expo(t,a,b):
    return b*np.exp(a*t)

def power(t,a,b):
    return b*t**a

from scipy.optimize import curve_fit
from_t = -50
pars, cov = curve_fit(f=expo, xdata=np.array(times2[from_t:-1]), ydata=mean2[from_t:-1], p0=[0.01,0.1], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=expo, xdata=np.array(times[from_t+20:-1]), ydata=mean[from_t+20:-1], p0=[0.01,0.1], bounds=(-np.inf, np.inf))
pars3, cov3 = curve_fit(f=power, xdata=np.array(times[from_t-200:from_t]), ydata=mean[from_t-200:from_t], p0=[0.01,0.1], bounds=(-np.inf, np.inf))


ax2.loglog(times, mean, 'k-', 
          markerfacecolor='none', label='High Oh',
          linewidth=4)

ax2.loglog(times2, mean2, 'b-', 
          markerfacecolor='none', label='Low Oh',
          linewidth=4)


tt = np.linspace(0.1,4.2,1000)
tt2 = np.linspace(5,80,1000)

ytt = expo(tt, *pars)
ytt2 = expo(tt, *pars2)
ytt3 = power(tt2, *pars3)

# Oh = 0.762
Oh = 0.289

times = [(len(mean)-j)/10 for j in range(len(mean))]


yt = [i**(0.42)/2 for i in tt]
yt2 = [i**(0.666)*10 for i in tt]
yt3 = [i**0.55/2 for i in tt]



ax2.plot(tt,ytt, 'y--', linewidth=3, label=r'$(t_b-t)^{0.42}$')

# ax2.plot(tt2,ytt3, 'c--', linewidth=3, label=r'$(t_b-t)^{0.6}$')
# print(pars3)

ax2.plot(tt,ytt2, 'y--', linewidth=3, label=r'$(t_b-t)$')

# ax.plot(tt,yt, 'b--', linewidth=3, label=r'$(t_b-t)^{0.42}$')
# ax.plot(tt,yt2, 'g--', linewidth=3, label=r'$(t_b-t)^{1/3}$')
# ax.plot(tt,yt3, 'y--', linewidth=3, label=r'$(t_b-t){0.0709/Oh}$')



x0 = np.linspace(.1,4.2,1000)
x1 = np.linspace(1.8,50,1000)
x2 = np.linspace(6,90,1000)

# y0 = [0.09*np.exp(i*0.012) for i in x0]
y1 = [i**0.418/16 for i in x1]
y2 = [(i**.666)/18 for i in x2]

ax2.plot([1, 20], [.75/5.75]*2, 'g--', label=r'$h_{min}=r_c$')


# ax2.plot(x0,y0, 'y--', linewidth=3, label=r'$0$')
ax2.plot(x1,y1, 'g--', linewidth=3, label=r'$\tau^{0.418}$')
ax2.plot(x2,y2, 'c--', linewidth=3, label=r'$\tau^{2/3}$')

ax2.set_ylabel(r'$h_{{min}}/R_0$')
ax2.set_xlabel(r'$(t_b-t)$')
# ax.set_ylim(0,1)
#  ax.set_xlabel(r'$t$')
ax2.legend(frameon=False)

plt.tight_layout()
# plt.savefig(f'low.pdf', dpi=dpi)


plt.show()
