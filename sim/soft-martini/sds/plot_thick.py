import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


convert_surfcon = 20**2/170**2

sc_lst =  []
del_lst = []

for entry in os.scandir('surfaceTension-mdpd/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        with open('/'.join([entry.path, f'interface.dat']), 'r') as fd:
            fd.readline()
            line = fd.readline()
            line = line.split(' ')
            con = float(line[1])*8.42
          
        del_lst.append(con)
        sc_lst.append(sc*convert_surfcon)

    except FileNotFoundError:
        print(f'interface.dat not found, skipping')
        continue




zip_lst = zip(sc_lst, del_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, del_lst = [list(tuple) for tuple in tuples]


fig, ax = plt.subplots(1,1)


#ax.errorbar([0]+sc_lst, [72]+gamma_lst, yerr = [std_lst[0]*0.9]+std_lst, fmt='o',
#ecolor = 'black', capsize= 2, capthick=1,color='black', label=r'MDPD')

ax.plot(sc_lst, del_lst, 'ko', label=r'MDPD')

# ax.plot([0]+sc_lst, [72]+gamma_lst, 'ko-', label='$\gamma$')
ax.set_xlabel(r'C [\AA$^{-2}$]')
#ax.set_xlim(-.1,1.9)
ax.set_ylabel(r'$\delta$ [\AA]')
#ax.set_ylim(20, 75)

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




sc_lst =  []
del_lst = []

for entry in os.scandir('surfaceTension-martini/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        with open('/'.join([entry.path, f'interface.dat']), 'r') as fd:
            fd.readline()
            line = fd.readline()
            line = line.split(' ')
            con = float(line[1])
            
        del_lst.append(con)
        sc_lst.append(sc*convert_surfcon)

    except FileNotFoundError:
        print(f'interface.dat not found, skipping')
        continue

zip_lst = zip(sc_lst, del_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, del_lst  = [list(tuple) for tuple in tuples]


#ax.errorbar(sc_lst, del_lst, yerr = std_lst, fmt='s',
#ecolor = 'blue', capsize= 2, capthick=1,color='blue', label=r'MD')

ax.plot(sc_lst, del_lst, 'bs' , label=r'MD')

lines, labels = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='lower right', frameon=False)

plt.tight_layout()
plt.savefig('thickness.pdf', dpi=dpi)
plt.show()


# fig2, ax2 = plt.subplots(1,1)

# ax2.plot(sc_lst, con_lst, 'ko-')

# ax2.set_xlabel(r'$C$ [$N_t/A_s$]')
# ax2.set_ylabel(r'$\Gamma$ [$N_s/A_s$]')

# plt.tight_layout()
# # plt.savefig('sc.pdf', dpi=dpi)

# plt.show()
