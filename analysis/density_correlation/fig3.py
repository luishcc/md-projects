import numpy as np

import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.5*side),
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


# r=5.7
r=4.8
#r=6

r = [4.8]*6
ri = [4.8, 4.8, 4.7, 4.7, 4.6, 4.4]

#ri=r

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
        q.append(float(line[0]) * 2 * np.pi * ri[iter])
        q_var.append(float(line[1]) * ( 2 * np.pi * ri[iter])**2)



plt.figure()
plt.plot(oh, x, label='Theory', linewidth=1.5, color='k', linestyle='--' )

plt.errorbar(oh_data[:], q, yerr = np.sqrt(q_var), fmt='o',ecolor = 'black',
color='black', label='Data', capsize=3, markerfacecolor='none')

# plt.title('Reduced Wavenumber')
plt.ylabel('$\chi$')
plt.xlabel(r'$Oh$')
plt.legend(loc=0)
# plt.grid(True)

plt.savefig('fig3.pdf', dpi=dpi, bbox_inches='tight')
plt.show()
