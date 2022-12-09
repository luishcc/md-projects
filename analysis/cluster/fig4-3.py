import numpy as np




################################################################################
################################################################################

# a = [50,60,70,80,85,90]
a = [0.266, .321, .451, .704, .901, 1.137]

# normal avg
# Main droplet peak
# b = [.297, .215, .210, .198, .135, .130]
# Different peaks
# b = [.373, .253, .242, .230, .148, .142]


# Break_avg
# Different peaks
b = [.355, .252, .233, .218, .139, .146] # sat/main
# b = [.282, .214, .201, .185, .126, .133] # sat/total
# b = [.200, .148, .163, .149, .086, .085] # sat/totals
b_var = [.0053, .0026, .0039, .0057, .0025, .0056]
# Main droplet peak
# b = [.205, .151, .163, .152, .088, .093] # sat/total

wave = [.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]
# wave = [1/i for i in wave]
wave = [i*2*np.pi*4.8 for i in wave]


lt = [.250, .210, .181, .158, .148,  .139]

lv = [0.581, .773, 1.499, 3.484, 6.8, 8.836]
# lv = [4.8/i for i in lv]

rho = [7.65, 8.30, 8.95, 9.6, 9.92, 10.24]
lr = [np.cbrt(1/i) for i in rho]


q_var = [3.156327982930347e-06,
2.328394395880221e-06,
1.8893985765694086e-06,
2.054396275751638e-06,
3.954677744054939e-06,
9.193559899539904e-06]
# q_var = [i*2*np.pi*4.8 for i in q_var]



a=wave
# a=lv
# a = [4.8**2/(i*j) for i, j in zip(lv, lt)]
# a = [3*4.8/(i) for i in lt]
# a = [x*(j/i) for x, i, j in zip(wave, lv, lt)]
a = [(i/j) for i, j in zip(lt, lv)]
# a = [4.8/j for x, j in zip(wave, lr)]
# a = lr

print(lv)
fit = np.polyfit(a,b, 1)
scale = (a[-1] - a[0]) * 0.5
a2 = np.linspace(a[0]-scale, a[-1]+scale, 100)
b_fit = [fit[0]*i + fit[1] for i in a2 ]

a2 = np.linspace(a[0]-scale, a[-1]+scale, 100)
fit2 = np.polyfit(a, b, 2)
b_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in a2 ]

def ff2(a):
    return fit2[0]*a**2 + fit2[1]*a +fit2[2]

def ff1(a):
    return fit[0]*a + fit[1]

def fexp(x,a,b):
    return a*np.exp(x*b)

def fpow(x,a,b):
    return a*x**b

from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=fpow, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))

stdevs = np.sqrt(np.diag(cov))
stdevs2 = np.sqrt(np.diag(cov2))

s1 = 0
s2 = 0
s3 = 0
s4 = 0
for i, j in enumerate(a):
    print(i,j)
    s1 += (ff1(j)-b[i])**2
    s2 += (ff2(j)-b[i])**2
    s3 += (fexp(j, *pars)-b[i])**2
    s4 += (fpow(j, *pars2)-b[i])**2

print(s1, s2, s3, s4)
print(fit, '\n', fit2)
print(pars, stdevs)
print(pars2, stdevs2)


import matplotlib as mpl
from matplotlib import container


dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (1.1*side, 1.1*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt

fig, axs = plt.subplots(ncols=1, nrows=1)
# gs = axs[0, 0].get_gridspec()
# for ax in axs[0, :]:
#     ax.remove()
# axbig = fig.add_subplot(gs[0, :])


# fig.tight_layout()

ax2 = axs


ax2.plot(a2, b_fit, 'k--', label='Linear fit')
# ax2.plot(a2, b_fit2, 'k--', label='Quadratic fit')
# ax2.plot(a2, fexp(a2, *pars), 'b--', label='exp fit')
# ax2.plot(a2, fpow(a2, *pars2), 'k--', label='$y=0.13x^{-0.5}$')
# ax2.plot(a, b, 'ko', label='Simulation')
ax2.errorbar(a, b, xerr = np.sqrt(q_var)*2*np.pi*4.8, yerr = np.sqrt(b_var),
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc='upper left', ncol=1)
ax2.set_ylabel('$N_{satellite}/N_{total}$')
# ax2.set_xlabel(r'$\chi$')
ax2.set_xlabel(r'$3R_0/l_T$')



# plt.savefig('fig4.pdf', bbox_inches='tight', dpi=dpi )


plt.show()
