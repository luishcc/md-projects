import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


def run_avg(file):
    sum = 0
    sumsq = 0
    n = 0
    with open(file, 'r') as fd:
        fd.readline()
        fd.readline()
        while True:
            line = fd.readline()
            try:
                a = float(line.split()[1])
            except:
                break
            sum += a
            sumsq += a**2
            n += 1
    avg = sum/n
    std = np.sqrt(sumsq/n - avg**2)
    return  avg, std

gamma_lst = []
sc_lst =  []
std_lst = []

for entry in os.scandir('surfaceTension-mdpd/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        gamma, std = run_avg('/'.join([entry.path, f'gamma_{sc}.profile']))
        gamma_lst.append(gamma)
        sc_lst.append(sc)
        std_lst.append(std)
    except FileNotFoundError:
        print(f'gamma_{sc}.profile not found, skipping')
        continue




zip_lst = zip(sc_lst, gamma_lst, std_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, gamma_lst, std_lst  = [list(tuple) for tuple in tuples]

const_conv = 300*1.380649/8.42**2 #KbT/rc^2 --> mN/m

gamma_lst = [const_conv*i for i in gamma_lst]
std_lst = [const_conv*i for i in std_lst]


fig, ax = plt.subplots(1,1)


ax.errorbar([0]+sc_lst, [72]+gamma_lst, yerr = [std_lst[0]*0.9]+std_lst, fmt='o',
ecolor = 'black', capsize= 2, capthick=1,color='black', label=r'MDPD')

# ax.plot([0]+sc_lst, [72]+gamma_lst, 'ko-', label='$\gamma$')
ax.set_xlabel(r'C [$N_t/A_s$]')
ax.set_xlim(-.1,1.9)
ax.set_ylabel(r'$\gamma$ [mN/m]')
ax.set_ylim(20, 75)

# ax.annotate('CMC', xy=(1.75, 21), xytext=(0.8, 21),
#             arrowprops=dict(facecolor='black', shrink=0.05))


# axx = ax.twinx()

# from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition)
# axx = plt.axes([0,0,1,1])
# ip = InsetPosition(axx, [0.18,0.18,0.8,0.8])
# axx.set_axes_locator(ip)

# ax.plot([1.8, 1.8], [18, 80], 'r--')


# axx.plot(sc_lst, con_lst, 'k^', markerfacecolor='none', label=r'$\Gamma$')
# axx.set_xlabel(r'$C$ [$N_t/A_s$]')
# axx.set_ylabel(r'$\Gamma$ [$N_s/A_s$]')
# axx.annotate('CMC', xy=(1.85, 1.3), xytext=(2.3, 1.5),
#             arrowprops=dict(facecolor='black', shrink=0.05))



gamma_lst = []
sc_lst =  []
std_lst = []

for entry in os.scandir('surfaceTension-martini/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        gamma, std = run_avg('/'.join([entry.path, f'gamma_{sc}.profile']))
        gamma_lst.append(gamma)
        sc_lst.append(sc)
        std_lst.append(std)
    except FileNotFoundError:
        print(f'gamma_{sc}.profile not found, skipping')
        continue

zip_lst = zip(sc_lst, gamma_lst, std_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, gamma_lst, std_lst  = [list(tuple) for tuple in tuples]


ax.errorbar(sc_lst, gamma_lst, yerr = std_lst, fmt='s',
ecolor = 'blue', capsize= 2, capthick=1,color='blue', label=r'MD')


lines, labels = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='upper right', frameon=False)

plt.tight_layout()
# plt.savefig('cmc.pdf', dpi=dpi)
plt.show()


# fig2, ax2 = plt.subplots(1,1)

# ax2.plot(sc_lst, con_lst, 'ko-')

# ax2.set_xlabel(r'$C$ [$N_t/A_s$]')
# ax2.set_ylabel(r'$\Gamma$ [$N_s/A_s$]')

# plt.tight_layout()
# # plt.savefig('sc.pdf', dpi=dpi)

# plt.show()
