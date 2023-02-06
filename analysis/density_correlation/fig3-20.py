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

oh = np.linspace(0.1, 2.30, 10000)
x = np.zeros(len(oh))

x = func(oh)

rho = [7.65, 8.30, 8.95, 9.6, 9.92, 10.24]
rho2 = [6.05, 6.9, 7.7, 8.4, 9.1, 9.5, 9.8]
rho3 = [ 6.75, 7.65, 8.30, 8.95, 9.6, 9.92, 10.24]


lr = {}
invlr = {}

lr[6] = [np.cbrt(1/i) for i in rho3]
invlr[6] = [1/i for i in lr[6]]
lr[4] = [np.cbrt(1/i) for i in rho3]
invlr[4] = [1/i for i in lr[4]]
lr[2] = [np.cbrt(1/i) for i in rho3]
invlr[2] = [1/i for i in lr[2]]

oh_r = {}
oh_r[6] = [.198, .266, .321, .451, .704, .901, 1.14]
oh_r[4] = [.243, .325, .393, .552, .863, 1.10, 1.39]
oh_r[2] = [.345, .460, .556, .781, 1.22, 1.56, 1.96]



A = [ 40, 50, 60, 70, 80, 85, 90]

R = [2, 4, 6]
scale_r = {2:.85, 4:.85, 6:.8}
radii_r = {2:[1.55, 1.5, 1.45, 1.41, 1.39, 1.36, 1.3],
           4:[3.2, 3.1, 3, 3, 2.9, 2.85, 2.8],
           6:[5.3, 5, 4.8, 4.5, 4.4, 4.35, 4.3]}
ratio = 48

oh_r[6] = [(oh**2*6/ri)**.5 for ri, oh in zip(radii_r[6], oh_r[6])]
oh_r[4] = [(oh**2*4/ri)**.5 for ri, oh in zip(radii_r[4], oh_r[4])]
oh_r[2] = [(oh**2*2/ri)**.5 for ri, oh in zip(radii_r[2], oh_r[2])]


q = {}
qinv = {}
q_var = {}
for r in R:
    q[r]=[]
    qinv[r]=[]
    q_var[r]=[]
    for i, a in enumerate(A):
        file = f'peak/R{r}_ratio{ratio}_A{a}-peak.csv'
        try:
            with open(file, 'r') as fd:
                fd.readline()
                line = fd.readline().split(',')
                q[r].append(float(line[0]) * 2 * np.pi * radii_r[r][i])
                qinv[r].append(1/(float(line[0]) *  radii_r[r][i]))
                q_var[r].append(float(line[1]) * ( 2 * np.pi * radii_r[r][i])**2)
        except Exception as e:
            print(e)
            continue

fig, ax = plt.subplots(1,1)

#
# ax2 = plt.axes([0,0,1,1])
# ip = InsetPosition(ax, [0.45,0.55,0.5,0.4])
# ax2.set_axes_locator(ip)

q[2] = [(i*21)/20 for i in q[2]]
q_var[2] = [(i*21)/20 for i, j in zip(q_var[2],q[2])]

ax.plot(oh, x, label='Theory', linewidth=1.5, color='k', linestyle='--' )

# plt.title('Reduced Wavenumber')
ax.set_ylabel('$\chi$')
ax.set_xlabel(r'Oh')
ax.set_ylim(0.22, 0.69)
ax.set_xlim(0.06, 2.31)


print(oh_r, q, q_var)

color = {2:'red', 4:'green', 6:'blue'}
marker = {2:'s', 4:'x', 6:'o'}
lstyle = {2:'-.', 4:'--', 6:'-'}

for r in R:
    # print(r)
    # print(oh_r[r], q[r], q_var[r])
    ax.errorbar(oh_r[r], q[r], yerr = np.sqrt(q_var[r]), fmt=marker[r],
    ecolor = color[r], color=color[r], label=f'$R_0={r}$',
    capsize=3, markerfacecolor='none')

    # q = qinv
    # q = [x**2 for x in q]
    # lr = [x**12 for x in lr]
    fit = np.polyfit(lr[r], q[r], 1)
    scale = (lr[r][-1] - lr[r][0]) * 0.1
    a2 = np.linspace(lr[r][0]-scale, lr[r][-1]+scale, 100)
    b_fit = [fit[0]*i + fit[1] for i in a2 ]

    fit2 = np.polyfit(lr[r], q[r], 2)
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
    pars, cov = curve_fit(f=fexp, xdata=lr[r], ydata=q[r], p0=[0, 0], bounds=(-np.inf, np.inf))
    pars2, cov2 = curve_fit(f=fpow, xdata=lr[r], ydata=q[r], p0=[0, 0], bounds=(-np.inf, np.inf))
    pars3, cov3 = curve_fit(f=flog, xdata=lr[r], ydata=q[r], p0=[0, 0], bounds=(-np.inf, np.inf))
    pars4, cov4 = curve_fit(f=fexp2, xdata=lr[r], ydata=q[r], p0=[9.29243653e+04, -2.66085321e+01, 6.43987070e-01], maxfev=100000)


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
        s1 += (ff1(j)-q[r][i])**2
        s2 += (ff2(j)-q[r][i])**2
        s3 += (fexp(j, *pars)-q[r][i])**2
        s4 += (fpow(j, *pars2)-q[r][i])**2
        s5 += (fpow(j, *pars3)-q[r][i])**2
        s6 += (fexp2(j, *pars4)-q[r][i])**2

    print(s1, s2, s3, s4, s5, s6)
    print(pars, stdevs)
    print(pars2, stdevs2)
    print(pars3, stdevs3)
    print(pars4, stdevs4)

    print(fit2[0], fit2[1], fit2[2])
    print(fit[0], fit[1])

    # ax2.set_ylabel(r'$\chi$')

    a2 = np.linspace(0.0, 0.8, 100)

    # ax2.errorbar(lr[r], q[r], yerr = np.sqrt(q_var[r])*0, fmt=marker[r],
    # ecolor = color[r],color=color[r], capsize=0, markerfacecolor='none')

    # ax2.plot(a2, [ff2(i) for i in a2], 'b--', label=r'$\chi = -35.9 \ l_{\rho}^2 + 38.5 \ l_{\rho} - 9.7 $')
        # ax2.plot(a2, [fexp2(i, *pars4) for i in a2], 'g--', label=r'$\chi = 0.701 - 1350e^{-18l_{\rho}}$')
    # ax2.plot(a2, [fexp2(i, *pars4) for i in a2], color=color[r],
    # linestyle=lstyle[r], label=rf'$R_0={r}$')

# ax2.plot([a2[0],a2[-1]], [0.697/4.8, 0.697/4.8], 'k-', label=r'0.697')
# ax2.plot([a2[0],a2[-1]], [0.697/1.7, 0.697/1.7], 'b-', label=r'0.697')
# ax2.plot([a2[0],a2[-1]], [0.697, 0.697], 'k-', label=r'0.697')

# ax2.set_xlabel(r'$l_{\rho}$')
# ax2.plot([0,1], [0,0], 'k-')
# ax2.set_xlim(0.45, 0.62)
# ax2.set_ylim(0.18, 0.75)
# ax2.set_ylim(0.23, 0.74)


# ax2.legend(loc='lower right', handlelength=1.5, borderaxespad=0.1, ncol=2,
#         columnspacing=0.6,  handletextpad=.2, fontsize=11, frameon=False)
# ax1.annotate(r'$\chi = -35.9 \ l_{\rho}^2 + 38.5 \ l_{\rho} - 9.7 $', xy=(0.48, 0.40) )

import matplotlib as mpl
from matplotlib import container
handles, labels = ax.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax.legend(handles, labels, loc='upper right', columnspacing=0.6,  handletextpad=.1,
frameon=False, ncol=2, fontsize=12, handlelength=1.5)

fig.tight_layout()
plt.savefig('fig3-222.pdf', dpi=dpi, bbox_inches='tight')

plt.show()
