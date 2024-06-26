import numpy as np

R = 8
rho = 5.8

a1 = [0, 0.5, 1.0, 1.6, 1.8, 2.0, 2.3, 2.6, 2.9, 3.4]
# a = [8*i/R for i in a1]  # beads / volume
a = [8*i/(8*i+R*rho) for i in a1]  # S-beads / Total beads


b =[18.3, 35, 59, 119, 111, 121, 133, 133, 173, 163]
b_var = []

c = [.28, .278, .201, .156, .12, .122, .06, .129, .15, .13]
# c = [.278, .221, .16, .14, .11, .18, .17, .26, .30]
c_var = [.007, 0.011, 0.022, 0.020, 0.023, 0.014, 0.03, 0.028, 0.05, 0.05]

d = [11.6, 16.46, 17.5, 23.3, 25.26, 25.9, 26, 28.7, 28.8, 31.1]


wave = [ 0.01338236354459586 * 2 * np.pi * R ] # 0 concentratino
wave_var = [ 2.408162556723014e-06 * 2 * np.pi * R**2 ]
for s in a1[1:]:
    # file = f'/home/luishcc/md-projects/analysis/density_correlation/peak/R{R}_{s}-peak.csv'
    file = f'/home/luishcc/md-projects/analysis/density_correlation/R{R}_{s}-peak.csv'
    try:
        with open(file, 'r') as fd:
            fd.readline()
            line = fd.readline().split(',')
            wave.append(float(line[0]) * 2 * np.pi * R)
            wave_var.append(float(line[1]) * ( 2 * np.pi * R**2))
    except Exception as e:
        print(e)
        continue


import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.7*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt
from matplotlib import container


fig, (ax1,ax2) = plt.subplots(ncols=1, nrows=2)

fig.subplots_adjust(hspace=.4)
# fig.subplots_adjust(wspace=.4)

ax1.plot(a,b, 'ko')
ax1.set_ylabel(r'$\Delta t_{Break}$')
ax1.set_xlabel(r'$C$  $[n/V]$')

ax2.errorbar(a, c, yerr=np.sqrt([i/20 for i in c_var]), fmt='.',
ecolor = 'black', color='black', label=f'$R_0={R}$',
capsize=3, markerfacecolor='none')
ax2.set_ylabel(r'$N_{satellite}/N_{total}$')
ax2.set_xlabel(r'$C$  $[n/V]$')




fig2, (ax3) = plt.subplots(ncols=1, nrows=1)
def pred4(x):
    return np.cbrt(1.5*np.pi/x)
x = np.linspace(wave[0], wave[-1], 100)
# ax3.plot(x, pred4(x), 'k--', label='Theory')

# ax3.errorbar(wave, [i/R for i in d], xerr=np.sqrt([i/20 for i in wave_var]), fmt='.',
# ecolor = 'black', color='black', label=f'$R_0={R}$',
# capsize=3, markerfacecolor='none')
# ax3.set_ylabel(r'$R/R_0$')
# ax3.set_xlabel(r'$\chi$')

ax4 = ax3
ax4.errorbar(a, [i/R for i in d], xerr=np.sqrt([i/20 for i in wave_var]), fmt='.',
ecolor = 'black', color='black', label=f'$R_0={R}$',
capsize=3, markerfacecolor='none')
ax4.set_ylabel(r'$R/R_0$')
ax4.set_xlabel(r'$C$  $[n/V]$')


fig.tight_layout()
fig.savefig('surf-time-prob.pdf', dpi=dpi)

fig2.tight_layout()
fig2.savefig('surf-size.pdf', dpi=dpi)

plt.show()
