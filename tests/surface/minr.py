import os
import sys


snap = 0
file = f'files/sc-{snap}.dat'
file2 = f'files2/sc-{snap}.dat'
file3 = f'files3/sc-{snap}.dat'
file4 = f'files4/sc-{snap}.dat'
file7 = f'files7/sc-{snap}.dat'
file6 = f'files6/sc-{snap}.dat'



min_r = []
min_z = []
snaps = []
min_r2 = []
min_z2 = []
snaps2 = []
min_r3 = []
min_z3 = []
snaps3 = []
# while os.path.isfile(file):
# end = 312
end = 2273
for i in range(end):
    lst_z = []
    lst_r = []
    with open(file6, 'r') as fd:
        fd.readline()
        fd.readline()
        for line in fd:
            line = line.split()
            lst_z.append(float(line[0]))
            lst_r.append(float(line[1]))
    min_r.append(min(lst_r)/4.4)
    min_z.append(lst_z[lst_r.index(min(lst_r))])
    snaps.append(snap)
    snap += 1
    file6 = f'files6/sc-{snap}.dat'

snap = 0
# while os.path.isfile(file):
# end2 = 2121 #files5
end2 = 1864
for i in range(end2):
    lst_z = []
    lst_r = []
    with open(file7, 'r') as fd:
        fd.readline()
        fd.readline()
        for line in fd:
            line = line.split()
            lst_z.append(float(line[0]))
            lst_r.append(float(line[1]))
    min_r2.append(min(lst_r)/4.4)
    min_z2.append(lst_z[lst_r.index(min(lst_r))])
    snaps2.append(snap)
    snap += 1
    file7 = f'files7/sc-{snap}.dat'

end3 = 1918
snap = 0
for i in range(end3):
    lst_z = []
    lst_r = []
    with open(file4, 'r') as fd:
        fd.readline()
        fd.readline()
        for line in fd:
            line = line.split()
            lst_z.append(float(line[0]))
            lst_r.append(float(line[1]))
    min_r3.append(min(lst_r)/4.4)
    min_z3.append(lst_z[lst_r.index(min(lst_r))])
    snaps3.append(snap)
    snap += 1
    file4 = f'files4/sc-{snap}.dat'

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import container
dpi = 1600
side = 5
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (1.8*side, 1.0*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, (ax) = plt.subplots(1,1, sharex = True)

ti = 10.703
ti=1
lt = 0.277
lv = 0.581

import numpy as np

x1 = np.linspace(0.01,0.2,100)
x2 = np.linspace(0.1,6.9,100)
x22 = np.linspace(0.2,.45,100)
x3 = np.linspace(.6,1.8,100)
x4 = np.linspace(1.7,2.6,100)
x5 = np.linspace(2.5,5.4,100)

y1 = [1/10 for i in x1]
y2 = [(i**0.418)/3.4 for i in x2]
y22 = [(i**(2/3))/3.4 for i in x2]
y3 = [(i)/3.4 for i in x2]
# y3 = [(i**(2/3))/3.1 for i in x3]
y4 = [(i)/4.2 for i in x4]
y5 = [(i**(.418))/2.8 for i in x5]


ax.loglog([(end2-i)/(10*ti) for i in snaps2], min_r2, 'b>', markerfacecolor='none', label='Low Oh')
ax.loglog([(end3-i)/(10*ti) for i in snaps3], min_r3, 'ko', markerfacecolor='none', label='High Oh')
ax.loglog([(end-i)/(10*ti) for i in snaps], min_r, 'gs', markerfacecolor='none', label='Surfactant')

# ax.plot(x1,y1, 'b--', linewidth=3.5,
    # label=r'$\displaystyle \frac{h_{min}}{R_0} \sim (t_b-t)^{0.418}$')

# ax.plot(x1*10,y1, 'g--', linewidth=3)
# ax.plot(x2*10,y2, 'g--', linewidth=3)
# ax.plot(x2*10,y22, 'g--', linewidth=3)
# ax.plot(x2*10,y3, 'g--', linewidth=3)
# ax.plot(x4*10,y4, 'g--', linewidth=3)
# ax.plot(x5,y5, 'b--', linewidth=3)


# ax.plot([0.1,100], [0.589]*2, 'r--')
# ax.plot([0.1,100], [0.277]*2, 'b--')
ax.plot([0.1,100], [0.152]*2, 'k--')
ax.plot([0.1,100], [0.152**.5*4.4**.5]*2, 'k--')
# ax.plot([1,5], [0.167]*2, 'k--')

# ax.plot([(end-i)/(10*ti) for i in snaps], [lv/6]*len(snaps), 'k--')

ax.set_ylabel(r'$h_{{min}}/R_0$')
ax.set_xlabel(r'$(t_b-t)^*$')

# ax.text(1.8, 0.34, r'$\displaystyle \frac{h_{min}}{R_0} \sim (t_b-t)^{0.418}$')
# ax.text(0.1, 0.29, r'$l_T \approx 0.277$')
# ax.text(0.1, 0.18, r'$l_T \approx 0.166$')
# ax.text(0.1, 0.6, r'$l_T \approx 0.589$')
# ax.text(6, 0.16, r'$l_{\rho} = 0.167$')

# ax.text(0.04, 0.09, r'$\tau^0$')
# ax.text(0.25, 0.13, r'$\tau^{2/3}$')
# ax.text(0.57, 0.19, r'$\tau^{0.418}$')
# ax.text(1.1, 0.3, r'$\tau^{2/3}$')
# ax.text(2.3, 0.46, r'$\tau^{1}$')
# ax.text(4.77, 0.6, r'$\tau^{0.418}$')

# ax.set_ylim(0.09,1.1)

ax.legend(frameon=False)

plt.tight_layout()
# plt.savefig(f'time.pdf', dpi=dpi)

plt.show()

exit()
from numpy import diff
from scipy import signal

snaps.reverse()
min_r.reverse()
x = np.array([((end-i)/(10*ti)) for i in snaps])
y = np.array(min_r)

dx = abs(x[1]-x[0])

y = signal.savgol_filter(y,20,4)

ddy = np.gradient(np.log(y),dx)
# ddx = diff(lnx)/dx
# ddx = np.gradient(np.log(x), dx)

# dy = signal.savgol_filter(dy*dx,20,3)
ddy = signal.savgol_filter(ddy,20,3)
# ddy = ddy*x

lnx = np.log(x)
lny = np.log(y)

fig, (ax, ax2, ax3) = plt.subplots(3,1)
ax.semilogx(x, lny)
ax2.plot(x, ddy)
ax3.plot(x, ddy*x)
plt.show()
