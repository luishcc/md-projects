import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 14,
    'figure.figsize': (1.2*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

convert_surfcon = 1              # In MDPD units (N/rc^-2)
convert_surfcon = 20**2/170**2   # From MDPD r_c^-2 to \AA^-2

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
del_lst = []

for entry in os.scandir('surfaceTension-mdpd/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        gamma, std = run_avg('/'.join([entry.path, f'gamma_{sc}.profile']))
        gamma_lst.append(gamma)
        sc_lst.append(sc*convert_surfcon)
        std_lst.append(std)
        with open('/'.join([entry.path, f'interface.dat']), 'r') as fd:
            fd.readline()
            line = fd.readline()
            line = line.split(' ')
            con = float(line[1])*8.42
        del_lst.append(con)
    except FileNotFoundError:
        print(f'gamma_{sc}.profile not found, skipping')
        continue


zip_lst = zip(sc_lst, gamma_lst, std_lst, del_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, gamma_lst, std_lst, del_lst  = [list(tuple) for tuple in tuples]

const_conv = 300*1.380649/8.42**2 #KbT/rc^2 --> mN/m

gamma_lst = [const_conv*i for i in gamma_lst]
std_lst = [const_conv*i for i in std_lst]


fig, (ax,ax2) = plt.subplots(1,2)


ax.errorbar([0]+sc_lst, [72]+gamma_lst, yerr = [std_lst[0]*0.9]+std_lst, fmt='o',
ecolor = 'black', capsize= 2, capthick=1,color='black', label=r'MDPD')

# ax.plot([0]+sc_lst, [72]+gamma_lst, 'ko-', label='$\gamma$')
ax.set_xlabel(r'C [\AA$^{-2}$]')
# ax.set_xlim(-.1,1.9)
ax.set_ylabel(r'$\gamma$ [mN/m]')
ax.set_ylim(20, 75)

# ax.annotate('CMC', xy=(1.75, 21), xytext=(0.8, 21),
#             arrowprops=dict(facecolor='black', shrink=0.05))

# ax.plot([1.8, 1.8], [18, 80], 'r--')


ax2.plot([0]+sc_lst, [0.53*8.42]+del_lst, 'ko', label=r'MDPD')
ax2.set_xlabel(r'C [\AA$^{-2}$]')
#ax2.set_xlim(-.1,1.9)
ax2.set_ylabel(r'$\delta$ [\AA]')
#ax2.set_ylim(20, 75)



gamma_lst = []
sc_lst =  []
std_lst = []
del_lst = []

for entry in os.scandir('surfaceTension-martini/sim'):
    if not entry.is_dir():
        continue
    try:
        sc = float(entry.name)
        gamma, std = run_avg('/'.join([entry.path, f'gamma_{sc}.profile']))
        gamma_lst.append(gamma)
        sc_lst.append(sc*convert_surfcon)
        std_lst.append(std)
        with open('/'.join([entry.path, f'interface.dat']), 'r') as fd:
            fd.readline()
            line = fd.readline()
            line = line.split(' ')
            con = float(line[1])
        del_lst.append(con)
    except FileNotFoundError:
        print(f'gamma_{sc}.profile or interface.dat not found, skipping')
        continue

zip_lst = zip(sc_lst, gamma_lst, std_lst, del_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, gamma_lst, std_lst, del_lst  = [list(tuple) for tuple in tuples]


ax.errorbar(sc_lst, gamma_lst, yerr = std_lst, fmt='s',
ecolor = 'blue', capsize= 2, capthick=1,color='blue', label=r'MD')


lines, labels = ax.get_legend_handles_labels()
ax.legend(lines, labels, loc='upper right', frameon=False)


ax2.plot(sc_lst, del_lst, 'bs' , label=r'MD')

lines, labels = ax2.get_legend_handles_labels()
ax2.legend(lines, labels, loc='lower right', frameon=False)


ax.annotate( 'a)',
        xy=(0, 1), xycoords='axes fraction',
        xytext=(-1.7, 0.2), textcoords='offset fontsize',
        fontsize='20', verticalalignment='top', fontfamily='serif',
        bbox=dict(facecolor='none', edgecolor='none', pad=3.0))

ax2.annotate( 'b)',
        xy=(0, 1), xycoords='axes fraction',
        xytext=(-1.7, 0.2), textcoords='offset fontsize',
        fontsize='20', verticalalignment='top', fontfamily='serif',
        bbox=dict(facecolor='none', edgecolor='none', pad=3.0))

plt.tight_layout()
plt.savefig('interface.pdf', dpi=dpi)
plt.show()

