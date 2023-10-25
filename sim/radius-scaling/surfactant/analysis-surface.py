import os
import sys 
from math import floor
import numpy as np
from scipy.optimize import curve_fit

from mdpkg.rwfile import DumpReader

dz = 2.
dr = 0.5

file =  'pinch_sc0.5.lammpstrj'
dir = '1'

datafile = '/'.join([dir,file])
save_dir = f'{dir}/surface_profile'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

trj = DumpReader(datafile)
trj.read_sequential()
trj.skip_next(452)
trj.read_next()

lz = trj.snap.box.get_length_z()
num_z = round(lz/dz)
dz = lz/num_z

lx = trj.snap.box.get_length_x()
num_r = round(0.5*lx/dr)
dr = lx/num_r

with open(f'{dir}/breaktime.txt', 'r') as fd:
    breaktime = int(fd.readline())

def f_rho(r, R0, D, p_l=6.05, p_v=0):
    t1 = 0.5 * (p_l + p_v)
    t2 = 0.5 * (p_l - p_v)
    t3 = np.tanh(2*(r - R0) / D)
    return t1 - t2 * t3

def gibbs_radius(rho):
    # pl = rho[0][2]
    pl = 6.05
    pv = 0
    r = []
    _rho = []
    for id, lst in sorted(rho.items()):
        r.append(lst[0])
        _rho.append(lst[2])
    print(_rho, r, rho)
    drho = np.gradient(_rho, r, edge_order=2)
    integral = [i**2*j*dr for i, j in zip(r,drho)]
    integral = sum(integral)
    print(integral/(pv-pl))
    return np.sqrt(integral/(pv-pl))

def fit_tanh(rho):
    r = []
    _rho = []
    for id, lst in sorted(rho.items()):
        r.append(lst[0])
        _rho.append(lst[2])    
    pars, cov = curve_fit(f=f_rho, xdata=r, ydata=_rho, p0=[8, 1], bounds=(-np.inf, np.inf))
    return pars

import matplotlib.pyplot as plt
x = np.linspace(0, lz, num_z)

for t in range(1, breaktime):
    plt.figure(1)
    print(t)

    r_l = []
    r_u = []
    r_b = []
    bins = {}
    snap = trj.snap
    print(snap.time)
    for atom in snap.atoms.values():
        idz = floor(abs(atom.position[2]*.999) / dz)
        bins.setdefault(idz, []).append(atom)

    for bin, atoms in sorted(bins.items()):

        print('\n', bin)

        center = [0,0]
        for atom in atoms:
            center[0] += atom.position[0]
            center[1] += atom.position[1]
        center[0] /= len(atoms)
        center[1] /= len(atoms)

        annuli = {}
        density = {}
        for atom in atoms:
            r = np.sqrt((atom.position[0]-center[0])**2 + (atom.position[1]-center[1])**2)
            idr = floor(r/dr)
            annuli.setdefault(idr, []).append(atom)
            density.setdefault(idr, [dr*(idr+0.5), (2*idr+1)*dr**2*dz*np.pi, 0])
            density[idr][2] += 1 / density[idr][1]
               
        # print(gibbs_radius(density))
        # R0, D = fit_tanh(density)
    
    #     print(R0, D)
    #     r_l.append(R0)
    #     r_u.append(R0 + D/2)
    #     r_b.append(R0 - D/2)
    
    # plt.plot(x, r_l)
    # plt.plot(x, r_u, 'k--')
    # plt.plot(x, r_b, 'k--')

    # plt.plot(x, [-i for i in r_l])
    # plt.plot(x,  [-i for i in r_u], 'k--')
    # plt.plot(x,  [-i for i in r_b], 'k--')

    plt.show()
    trj.read_next()

    print()
    print(t)



