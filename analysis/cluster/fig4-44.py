import numpy as np




################################################################################
################################################################################

# a = [50,60,70,80,85,90]
a = [.311, .311, .266, .266, .266]; xlabel = '$Oh$'

b = [.076, .180, .411, .389, .296] # sat/main

# Break_avg
# Different peaks
# b = [.411, .389, .355, .252, .233, .218, .139, .146] # sat/main
b_var = [.00, .00, .004, .006, .0053]

wave = [1, 1, .011887547350585061, .01338236354459586,
.018927425365090515]

radii = [2, 4, 10, 8, 6 ]
radii = [r*0.8 for r in radii]

wavelen = [1/i for i in wave]
red_wavenum = [i*2*np.pi*r for i,r in zip(wave,radii)]


lt = [.277, .277, .250, .250, .250]

lv = [.581, .581, 0.426, 0.426, 0.426]
# lv = [4.8/i for i in lv]

rho = [6.95, 6.95, 7.65, 7.65, 7.65]
lr = [np.cbrt(1/i) for i in rho]


q_var = [0, 0, 3.990705611232144e-06, 2.408162556723014e-06,
3.156327982930347e-06]
# q_var = [i*2*np.pi*r*0.8 for i,r in zip(q_var,radii)]



# a = wavelen ; xlabel = '$\lambda$'
# a = red_wavenum ; xlabel = '$\chi$'
# a = lv ; xlabel = '$L_v$'
# a = lt ; xlabel = '$L_t$'
# a = lr ; xlabel = '$L_r$'

# a = [1/i**2 for i in a] ; xlabel = '$Oh^{-2}$'

# a = [(i/j) for i, j in zip(lt, lv)]; xlabel = '$L_v/L_T$'
# a = [(i/j) for i, j in zip(lr, lv)]; xlabel = '$L_r/L_T$'
# a = [r/(i) for i,r in zip(lt,radii)]; xlabel = '$R_0/L_T$'
# a = [r/(i) for i,r in zip(lv,radii)]; xlabel = '$R_0/L_v$'

a = [r**1 for r in radii]; xlabel = '$R_0$'

# a = [r**2/(i*j) for r, i, j in zip(radii, lv, lt)]; xlabel = '$R_0^{2}/L_vL_T$'
# a = [(r**2/(i*j))**0.5 for r, i, j in zip(radii, lv, lt)]; xlabel = '$R_0/\sqrt{L_vL_T}$'
# a = [((j/i)/x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$L_v/\lambda L_T$'
# a = [((j/i)*x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda L_v/ L_T$'
# a = [(x**2/(i*j))**0.5 for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda^2/ L_v L_T$'
# a = [(x) for x, i, j in zip(wave, lv, lt)] ; xlabel = '$1/\lambda $'
# a = [x*(i/j) for x, i, j in zip(red_wavenum, lv, lt)] ; xlabel = '$\chi L_T/L_v$'
# a = [(r*p)/(i*j) for r,p,  i, j in zip(radii,  lr, lv, lt)] ; xlabel = '$RL_T/L_pL_v$'
# a = [x/i for x, i in zip(wave, lv)] ; xlabel = '$L_v/\lambda$'
# a = [r/x for x, r in zip(wave, radii)]; xlabel = '$R_0/\chi$'


scale = (max(a) - min(a)) * 0.5
lla = min(a)
ula = max(a)
scale = (ula-lla)*0.2
a2 = np.linspace(lla-scale, ula+scale, 100)

fit = np.polyfit(a,b, 1)
b_fit = [fit[0]*i + fit[1] for i in a2 ]

fit2 = np.polyfit(a, b, 2)
b_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in a2 ]

def ff2(a):
    return fit2[0]*a**2 + fit2[1]*a +fit2[2]

def ff1(a):
    return fit[0]*a + fit[1]

def fexp(x,a,b):
    return a*np.exp(x*b)

def fexp2(x,a,b,c):
    return c-a*np.exp(x*b)

def fpow(x,a,b):
    return a*x**b

from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=fpow, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))
pars4, cov4 = curve_fit(f=fexp2, xdata=a, ydata=b, maxfev=10000)


stdevs = np.sqrt(np.diag(cov))
stdevs2 = np.sqrt(np.diag(cov2))
stdevs4 = np.sqrt(np.diag(cov4))


s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
for i, j in enumerate(a):
    print(i,j)
    s1 += (ff1(j)-b[i])**2
    s2 += (ff2(j)-b[i])**2
    s3 += (fexp(j, *pars)-b[i])**2
    s4 += (fpow(j, *pars2)-b[i])**2
    s5 += (fexp2(j, *pars4)-b[i])**2

print(s1, s2, s3, s4, s5)
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


ax2.loglog(a2, b_fit, 'k--', label='Linear fit')
ax2.plot(a2, b_fit2, 'b--', label='Quadratic fit')
# ax2.plot(a2, fexp2(a2, *pars4), 'y--', label='exp fit')
ax2.plot(a2, fpow(a2, *pars2), 'g--', label='pow')
# ax2.plot(a, b, 'ko', label='Simulation')
ax2.errorbar(a, b, xerr = np.sqrt(q_var)*2*np.pi*4.8, yerr = np.sqrt(b_var),
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc='upper left', ncol=1)
ax2.set_ylabel('$N_{satellite}/N_{main}$')
ax2.set_xlabel(xlabel)
# ax2.set_xlabel(r'$3R_0/l_T$')



# plt.savefig('fig4.pdf', bbox_inches='tight', dpi=dpi )


plt.show()
