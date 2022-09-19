import numpy as np
import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.85*side, 0.55*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt

def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)

oh = np.linspace(0.2, 1.30, 10000)
x = np.zeros(len(oh))

x = func(oh)

# for i in range(len(oh)):
#     x[i] = func(oh[i])


# r=5.7
r=4.8
#r=6


R = 6
ratio = 48

A = [50, 60, 70, 80, 85, 90]
oh_data = [0.266,0.321,0.451,0.704,0.901,1.137]

q = []
q_var = []
for iter, a in enumerate(A[:]):
    file = f'R{R}_ratio{ratio}_A{a}-peak.csv'
    with open(file, 'r') as fd:
        fd.readline()
        line = fd.readline().split(',')
        q.append(float(line[0])*2*np.pi*r)
        q_var.append(float(line[1]))


q_var = np.array(q_var)

fig, ax = plt.subplots(1,1)
ax.plot(oh, x, 'k--', label='Theory')

ax.errorbar(oh_data[:], q, yerr = np.sqrt(q_var)*2*np.pi*r,
fmt='o',ecolor = 'black',color='black', label='Simulation')

ax.set_ylabel(r'$\chi$')
ax.set_xlabel(r'$Oh$')
from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax.legend(handles, labels, loc='upper right')

# plt.legend(loc=0)
plt.show()
