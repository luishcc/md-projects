import os

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)


from mdpkg.rwfile import read_dat


# r6 = [0.017699, 0.019868, 0.015957, 0.017699,
#         0.018939, 0.019933, 0.017699, 0.018785, 0.01657]
# xr6 = [226, 301, 376, 452, 527, 603, 904, 1809, 1809]


r6 = [0.017699, 0.018868, 0.016257, 0.017699,
        0.018339, 0.019133, 0.017699, 0.017685]

r6 = [0.017699, 0.018868, 0.017699,
        0.018339, 0.017699, 0.017685]

# r6 = [0.017699, 0.019868, 0.015957, 0.017699,
#         0.018939, 0.019933, 0.017699, 0.017685]

# xr6 = [226, 301, 376, 452, 527, 603, 904, 1809]
xr6 = [226, 301,  452, 527,  904, 1809]


r8 = [0.013245, 0.013289, 0.013267]
xr8 = [301, 603, 1206]

r10 = [0.010638, 0.010610]
r10 = [0.010638, 0.010610]
xr10 = [376, 753]

xr6 = [l/(2*np.pi*6) for l in xr6]
xr8 = [l/(2*np.pi*8) for l in xr8]
xr10 = [l/(2*np.pi*10) for l in xr10]


snap = 160

R = 6
ratio = 48
A = -50
grid = 1
sim_case = f'R{R}_ratio{ratio}_A{abs(A)}'

path_to_data = os.getcwd()
dir = '/'.join([path_to_data, sim_case])

file_correlation = dir + f'/{snap}.dat'
file_fourier = '/'.join([dir, 'fourier', f'{snap}.dat'])

# print(file)
data = read_dat(file_correlation)
data_f = read_dat(file_fourier)

fig, [ax1, ax] = plt.subplots(2,1, gridspec_kw={'height_ratios': [1.5, 1]})

ax2 = plt.axes([0,0,1,1])
ip = InsetPosition(ax1, [0.45,0.45,0.5,0.4])
ax2.set_axes_locator(ip)
# mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.5')

skip_f = 3
for i in range(5, 6):
    # print(data[str(i-1)])
    if not np.any(np.isnan(data[str(i-1)])):
        ax2.plot([k/1809 for k in data['dz']], data[str(i-1)],  label=f'r={i-1}')
        ax1.plot(data_f['freq'][skip_f:], data_f[str(i-1)][skip_f:],  label=f'r={i-1}')


red = np.array([6,8,10]) * 2*np.pi *0.88
# red = [1,1,1]


ax.set_ylabel(r'$\chi$')

ax.plot(xr6, [i*red[0] for i in r6], 'ko--', markersize=7.5, markerfacecolor='none', label=r'$R_0=6$')
ax.plot(xr8, [i*red[1] for i in r8], 'bx--', markersize=9.5, markerfacecolor='none',label=r'$R_0=8$')
ax.plot(xr10, [i*red[2] for i in r10], 'gs--', markersize=8.5, markerfacecolor='none',label=r'$R_0=10$')
ax.set_ylim(0.4,0.7)
ax.legend(loc=(0.55, 0.05))
ax.set_xlabel('$L/2\pi R_0$')

# Some ad hoc tweaks.
ax1.set_ylim(0,9)
ax1.set_xlim(0,0.1)
ax1.set_xlabel('q')
ax1.set_ylabel('Ĝ(r,q)')

ax2.set_ylim(0.3,0.8)
ax2.set_xlabel('dz/L')
ax2.set_ylabel('G(r,dz)')


# ax2.set_yticks(np.arange(0,2,0.4))
# ax2.set_xticklabels(ax2.get_xticks(), backgroundcolor='w')
# ax2.tick_params(axis='x', which='major', pad=8)

plt.show()
#
# plt.xlabel(r'$\delta z$')
# plt.ylabel(r'$G(r,\delta z)$')
# plt.title(f'R_0 = {R}, Ratio = {ratio}, Snapshot = {snap}')
# plt.ylim(-0.05, 1.1)
# # plt.xlim(0, 110)
# plt.plot([0, data['dz'][-1]], [0, 0], 'k--')
# plt.legend(loc='right')
# plt.savefig(f'{dir_out}/{snap}.png', format='png')
# # plt.show(block=False)
# plt.close(1)
# snap += 1
# file = dir + f'/{snap}.dat'
