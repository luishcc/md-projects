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
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)


def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)

oh = np.linspace(0.2, 1.30, 10000)
x = np.zeros(len(oh))

x = func(oh)

rho = [7.65, 8.30, 8.95, 9.6, 9.92, 10.24]
lr = [np.cbrt(1/i) for i in rho]
invlr = [1/i for i in lr]

# r=5.7
r=4.8
#r=6

r = [4.8]*6
ri = [4.8, 4.8, 4.7, 4.7, 4.6, 4.4]

ri=r

R = 6
ratio = 48

A = [50, 60, 70, 80, 85, 90]
oh_data = [0.266,0.321,0.451,0.704,0.901,1.137]

q = []
qinv = []
q_var = []
for iter, a in enumerate(A[:]):
    file = f'peak/R{R}_ratio{ratio}_A{a}-peak.csv'
    with open(file, 'r') as fd:
        fd.readline()
        line = fd.readline().split(',')
        q.append(float(line[0]) * 2 * np.pi * ri[iter])
        qinv.append(1/(float(line[0]) * ri[iter]))
        q_var.append(float(line[1]) * ( 2 * np.pi * ri[iter])**2)


fig, ax = plt.subplots(1,1)


ax2 = plt.axes([0,0,1,1])
ip = InsetPosition(ax, [0.45,0.55,0.5,0.4])
ax2.set_axes_locator(ip)



ax.plot(oh, x, label='Theory', linewidth=1.5, color='k', linestyle='--' )

ax.errorbar(oh_data[:], q, yerr = np.sqrt(q_var), fmt='o',ecolor = 'black',
color='black', label='Simulation', capsize=3, markerfacecolor='none')

# plt.title('Reduced Wavenumber')
ax.set_ylabel('$\chi$')
ax.set_xlabel(r'$Oh$')
ax.set_ylim(0.3, 0.85)
ax.legend(loc='lower left', frameon=False)

# q = qinv
# q = [x**2 for x in q]
# lr = [x**12 for x in lr]
fit = np.polyfit(lr, q, 1)
scale = (lr[-1] - lr[0]) * 0.1
a2 = np.linspace(lr[0]-scale, lr[-1]+scale, 100)
b_fit = [fit[0]*i + fit[1] for i in a2 ]

fit2 = np.polyfit(lr, q, 2)
b_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in a2 ]

def ff2(a):
    return fit2[0]*a**2 + fit2[1]*a +fit2[2]

def ff1(a):
    return fit[0]*a + fit[1]

def fexp(x,a,b):
    return a*np.exp(x*b)

def fexp2(x,a,b,c):
    return c-a*np.exp(x*b)

def flog(x,a,b):
    return a*np.log(x) + b

def fpow(x,a,b):
    return a*x**b

from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=lr, ydata=q, p0=[0, 0], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=fpow, xdata=lr, ydata=q, p0=[0, 0], bounds=(-np.inf, np.inf))
pars3, cov3 = curve_fit(f=flog, xdata=lr, ydata=q, p0=[0, 0], bounds=(-np.inf, np.inf))
pars4, cov4 = curve_fit(f=fexp2, xdata=lr, ydata=q, maxfev=10000)


stdevs = np.sqrt(np.diag(cov))
stdevs2 = np.sqrt(np.diag(cov2))
stdevs3 = np.sqrt(np.diag(cov3))
stdevs4 = np.sqrt(np.diag(cov4))


s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
s6 = 0
for i, j in enumerate(lr):
    print(i,j)
    s1 += (ff1(j)-q[i])**2
    s2 += (ff2(j)-q[i])**2
    s3 += (fexp(j, *pars)-q[i])**2
    s4 += (fpow(j, *pars2)-q[i])**2
    s5 += (fpow(j, *pars3)-q[i])**2
    s6 += (fexp2(j, *pars4)-q[i])**2

print(s1, s2, s3, s4, s5, s6)
print(pars, stdevs)
print(pars2, stdevs2)
print(pars3, stdevs3)
print(pars4, stdevs4)

print(fit2[0], fit2[1], fit2[2])
print(fit[0], fit[1])

ax2.set_ylabel(r'$\chi$')

a2 = np.linspace(0.0, 0.8, 100)
ax2.plot([a2[0],a2[-1]], [0.697, 0.697], 'k-', label=r'0.697')
# ax1.plot(lr, q, 'ko', label='Simulation')
ax2.errorbar(lr, q, yerr = np.sqrt(q_var), fmt='o',ecolor = 'black',
color='black', capsize=3, markerfacecolor='none')
# ax1.plot(a2, [ff1(i) for i in a2], 'k-', label='Linear')
# ax2.plot(a2, [ff2(i) for i in a2], 'b--', label=r'$\chi = -35.9 \ l_{\rho}^2 + 38.5 \ l_{\rho} - 9.7 $')
# ax1.plot(a2, [fexp(i, *pars) for i in a2], 'b-', label='Exponential')
# ax2.plot(a2, [fexp2(i, *pars4) for i in a2], 'g--', label=r'$\chi = 0.701 - 1350e^{-18l_{\rho}}$')
ax2.plot(a2, [fexp2(i, *pars4) for i in a2], 'g-.', label=r'Fit')
# ax1.plot(a2, [fpow(i, *pars2) for i in a2], 'b--', label='Power')
# ax1.plot(a2, [flog(i, *pars3) for i in a2], 'b--', label='Log')
ax2.set_xlabel(r'$l_{\rho}$')
# ax2.plot([0,1], [0,0], 'k-')
ax2.set_xlim(0.44, 0.65)
ax2.set_ylim(0.3, 0.75)
ax2.legend(loc='lower right', handlelength=1.5, borderaxespad=0.1,
        columnspacing=1, fontsize=12, frameon=False)
# ax1.annotate(r'$\chi = -35.9 \ l_{\rho}^2 + 38.5 \ l_{\rho} - 9.7 $', xy=(0.48, 0.40) )


fig.tight_layout()
plt.savefig('fig3-2.pdf', dpi=dpi, bbox_inches='tight')

plt.show()
