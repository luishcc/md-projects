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

con_lst = []
sc_lst =  []

for entry in os.scandir('sim'):
    if not entry.is_dir():
        continue
    
    sc = float(entry.name)
    sc_lst.append(sc)
  
    with open(f'{entry.path}/interface.dat', 'r') as fd:
        fd.readline()
        line = fd.readline()
        line = line.split(' ')
        con = float(line[1])
    con_lst.append(con)


zip_lst = zip(sc_lst,  con_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
sc_lst, con_lst = [list(tuple) for tuple in tuples]


fig, ax = plt.subplots(1,1)

ax.set_xlabel(r'C [$N_t/A_s$]')
ax.set_ylabel(r'$\delta$ [$r_c$]')
# ax.set_ylim(20, 75)

ax.plot(sc_lst, con_lst, 'k-')


plt.tight_layout()
plt.savefig('th.pdf', dpi=dpi)
plt.show()

