import numpy as np

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())
    return snap

def read_sim(dir):
    min_r = []
    min_z = []
    breaktime = get_breaktime(dir)
    for i in range(breaktime):
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
    print(i, breaktime, i-breaktime, dir)
    return min_r, [abs(z-z0) for z in min_z], len(min_r)

import matplotlib.pyplot as plt
import matplotlib as mpl

dpi = 1600
side = 7
fontsize = 24
rc_fonts = {
    "font.family": "serif",
    "font.size": fontsize,
    'figure.figsize': (0.8*side, .7*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, ax2 = plt.subplots(1,1, sharex = False)

lists = []

nn=20

sc = 1.0

case = f'/home/luishcc/hdd/radius_scaling/surfactant/{sc}'

for i in range(nn):
    if i ==  114  :
        continue
    r, z, t = read_sim(f'{case}/{i+1}')
    lists.append(r)
    ax2.loglog([(t-j) for j in range(t)], r, 'c--',
              linewidth=1, markerfacecolor='gray')

mean = []
for i in range(max([len(l) for l in lists])):
    temp = []
    for lst in lists:
        if len(lst) > i:
            temp.append(lst[-i-1])
    mean.append(sum(temp)/len(temp))
mean.reverse()


ax2.plot([(len(mean)-j) for j in range(len(mean))], mean, 'ko', 
          markerfacecolor='black', label='Average',
          linewidth=3)


ax2.plot([1, 50], [1/8.1]*2, 'k--')
ax2.text(20, 0.09, r'$h_{min} = r_c$', fontsize=0.8*fontsize)

ax2.text(65, 0.04, rf'$C = {sc}$', fontsize=0.8*fontsize)

ax2.set_xlim(0.7, 1000)

times = [(len(mean)-j) for j in range(len(mean))]

tt = np.linspace(0,80,1000)
tt2 = np.linspace(0,150,1000)

x0 = np.linspace(1,12,1000)
x2 = np.linspace(5, 200,1000)
x3 = np.linspace(5,200,1000)

y0 = [np.exp(0.08*i)/15 for i in x0]
y2 = [(i**.666)/28 for i in x2]
y3 = [(i**.418)/22 for i in x3]

ax2.plot(x0,y0, 'y--', linewidth=2.5, label=r'$\sim e^{\tau}$')
ax2.plot(x2,y2, 'b--', linewidth=2.5, label=r'$\sim \tau^{0.666}$')
ax2.plot(x3,y3, 'g--', linewidth=2.5, label=r'$\sim \tau^{0.418}$')

ax2.set_ylabel(r'$h_{{min}}/R_0$')
ax2.set_xlabel(r'$\tau$')

ax2.set_ylim(0.03,1.3)
ax2.legend(frameon=False, loc='upper left',  handlelength=1.5, borderaxespad=0.1, ncol=1,
         columnspacing=0.6,  handletextpad=.2, fontsize=0.7*fontsize)

plt.tight_layout()
plt.savefig(f'surfactant-{sc}.pdf', dpi=dpi)

plt.show()

################################################################
################################################################

# from scipy.signal import savgol_filter

# plt.figure()

# mean2 = savgol_filter( mean, 4, 1)
# # mean2 = mean

# dy = np.gradient(np.log(mean2), np.log(times), edge_order=2)
# w = savgol_filter( dy, 50, 4)

# plt.semilogx(times, dy)
# plt.plot(times, w)

# plt.ylim(-0.2,0.8)

# plt.show()
