import os
import sys
import numpy as np
from math import floor

from mdpkg.rwfile import Dat, CSV, read_dat, DumpReader
from mdpkg.grid import GridSurf


try:
    sc = sys.argv[1]
    file = '/'.join(['sim', sc, f'sim_{sc}.lammpstrj'])
except Exception as e:
    print(e)
    sc = '0.1'
    file = 'sim/0.1/sim_0.1.lammpstrj'

trj = DumpReader(file)
trj.read_sequential()
trj.skip_next(10)
trj.read_next()

num = 200
data = np.zeros((num,4))

lx = trj.snap.box.get_length_x()
ly = trj.snap.box.get_length_y()
lz = trj.snap.box.get_length_z()

sz  = lz/num
vol = lx * ly * sz
ivol = 1/vol

area = 2 * lx * ly
iarea = 1/area
con = 0

count=0
while True:
    print(count)
    for atom in trj.snap.atoms.values():
        z = atom.position[2] + lz/2
        idz = floor(z/sz)
        type = int(atom.type)
        if idz >= num:
            data[num-1][0] += ivol
            data[num-1][type] += ivol
            continue
        elif idz < 0:
            data[0][0] += ivol
            data[0][type] += ivol
            continue
        data[idz][0] += ivol
        data[idz][type] += ivol        
        if  (z > 43 or z < 27) and type !=3:
            con += iarea
    count += 1
    try:
        trj.read_next()
    except Exception as e:
        print(e)
        break

data = data/count

import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


def rho(z,  r, d):
    return 6.05*0.5*(1-np.tanh(2*(z-r)/d))

num2=50
ini = floor(len(data)/2)
from scipy.optimize import curve_fit
pars, cov = curve_fit(f=rho, 
                      xdata=np.linspace(0,num2,num2)*sz, 
                      ydata=data[ini:ini+num2,3], 
                      p0=[10, 2], bounds=(-np.inf, np.inf))

print(pars)
# with open(f'sim/{sc}/interface.dat', 'w') as fd:
#     fd.write('R0 thickness\n')
#     fd.write(f'{pars[0]} {pars[1]}')


con_lst = []
sc_lst =  []

for entry in os.scandir('sim'):
    if not entry.is_dir():
        continue
    
    scc = float(entry.name)
    sc_lst.append(scc)
  
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



stdevs = np.sqrt(np.diag(cov))


z = np.linspace(-lz/2,lz/2,num)



# exit()

fig, axx = plt.subplots(1,1)

from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition)
ax = plt.axes([0,0,1,1])
ip = InsetPosition(ax, [0.35,0.18,0.62,0.65])
ax.set_axes_locator(ip)


axx.set_xlabel(r'C [$N_t/A_s$]')
axx.set_ylabel(r'$\delta$ [$r_c$]')
axx.plot(sc_lst, con_lst, 'kx', markerfacecolor='none')

axx.annotate('CMC', xy=(1.7, 1.9), xytext=(0.8, 1.8),
            arrowprops=dict(facecolor='black', shrink=0.05))



ax.plot(z, data[:,3], 'b-', label='W', markerfacecolor='none')
ax.plot(z, data[:,1], 'r-o', label='H', markerfacecolor='none')
ax.plot(z, data[:,2], 'g-s', label='T', markerfacecolor='none')

ax.plot([pars[0]]*2, [0,6], 'k-.')
ax.plot([pars[0]-pars[1]*0.5]*2, [0,6], 'k--')
ax.plot([pars[0]+pars[1]*0.5]*2, [0,6], 'k--')

# ax.set_xlim(-20, 20)
ax.set_xlim(6, 13.5)
ax.set_ylim(-0.02, 6.2)
ax.set_ylabel(r'$\rho$ $[N/V]$')
ax.set_xlabel(r'$z$ [$r_c$]')

# ax.text(pars[0],6.5, fr'$R_0$')
# ax.text(pars[0],6.5, fr'$\delta_0$')

ax.legend(frameon=False, loc='center left')

plt.tight_layout()
plt.savefig(f'dense-{sc}.pdf', dpi=dpi)
plt.show()
