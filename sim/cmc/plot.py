import os
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.9*side),
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
con_lst = []
sc_lst =  []
std_lst = []

for entry in os.scandir('sim'):
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
    with open(f'{entry.path}/sc.dat', 'r') as fd:
        con = float(fd.readline())
    con_lst.append(con)


zip_lst = zip(sc_lst, gamma_lst, std_lst, con_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, gamma_lst, std_lst, con_lst = [list(tuple) for tuple in tuples]

gamma_lst = [(72/7.62)*i for i in gamma_lst]
std_lst = [(72/7.62)*i for i in std_lst]

fig, ax = plt.subplots(1,1)

ax.errorbar([0]+sc_lst, [72]+gamma_lst, yerr = [std_lst[0]*0.9]+std_lst, fmt='o',
ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')

ax.plot([0]+sc_lst, [72]+gamma_lst, 'ko-')
ax.set_xlabel(r'C [$N_t/A_s$]')
ax.set_ylabel(r'$\gamma$ [mN/m]')

plt.tight_layout()
plt.savefig('cmc.pdf', dpi=dpi)

fig2, ax2 = plt.subplots(1,1)

ax2.plot(sc_lst, con_lst, 'ko-')

ax2.set_xlabel(r'$C$ [$N_t/A_s$]')
ax2.set_ylabel(r'$\Gamma$ [$N_s/A_s$]')

plt.tight_layout()
plt.savefig('sc.pdf', dpi=dpi)

plt.show()
