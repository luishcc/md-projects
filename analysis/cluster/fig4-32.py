import numpy as np


end = 1

################################################################################
################################################################################

a = [.538, .380, .311,  # A=-50 new W_p
     .621, .439, .359,  # A=-60 new W_p
     .864, .611,        # A=-70 new W_p
     1.32, .933,        # A=-80 new W_p
     1.66, 1.18,        # A=-85 new W_p
     2.01,              # A=-90 new W_p
     .206, .230, .266, .321, .451, .704, .901, 1.137]; xlabel = '$Oh$'

# normal avg
# Different peaks
b = [.074, .160, .285,
     .046, .139, .220,
     .049, .133,
     .026, .110,
     .038, .095,
     .0,
     .406, .380, .296, .215, .210, .196, .135, .130] # sat/main


# Break_avg
# Different peaks
# b = [.069, .180, .276,
#      .046, .144, .229,
#      .049, .137,
#      .026, .106,
#      .038, .093,
#      .0,
#      .411, .389, .282, .213, .200, .183, .126, .133] # sat/main

b_var = [.003, .005, .006,
         .002, .007, .006,
         .003, .004,
         .001, .004,
         .004, .0,
         .000,
         .004, .006, .0053, .0026, .0039, .0057, .0025, .0056]


wave = [.1, .1, .1,
        .1, .1, .1,
        .1, .1,
        .1, .1,
        .1, .1,
        .1,
.011887547350585061, .01338236354459586,
.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]

radii = [2, 4, 6,
         2, 4, 6,
         2, 4,
         2, 4,
         2, 4,
         2,
         10, 8, 6, 6, 6, 6, 6, 6]
# radii = [r*0.8 for r in radii]

wavelen = [1/i for i in wave]
red_wavenum = [i*2*np.pi*r for i,r in zip(wave,radii)]


lt = [.277, .277, .277,
      .227, .227, .227,
      .193, .193,
      .166, .166,
      .154, .154,
      .145,
      .250, .250, .250, .210, .181, .158, .148, .139]

lv = [.581, .581, .581,
      .773, .773, .773,
      1.499, 1.499,
      3.484, 3.484,
      5.545, 5.545,
      8.839,
      .426, .426, .426, .617, 1.224, 2.97, 4.87, 7.75]
# lv = [4.8/i for i in lv]

rho = [6.95, 6.95, 6.95,
       7.7, 7.7, 7.7,
       8.4, 8.4,
       9.1, 9.1,
       9.5, 9.5,
       9.8,
       7.65, 7.65, 7.65, 8.30, 8.95, 9.6, 9.92, 10.24]
lr = [np.cbrt(1/i) for i in rho]


q_var = [0, 0, 0,
         0, 0, 0,
         0, 0,
         0, 0,
         0, 0,
         0,
3.990705611232144e-06,
2.408162556723014e-06,
3.156327982930347e-06,
2.328394395880221e-06,
1.8893985765694086e-06,
2.054396275751638e-06,
3.954677744054939e-06,
9.193559899539904e-06]
# q_var = [i*2*np.pi*r*0.8 for i,r in zip(q_var,radii)]



# a = wavelen ; xlabel = '$\lambda$'
# a = red_wavenum ; xlabel = '$\chi$'
# a = lv ; xlabel = '$L_v$'
# a = lt ; xlabel = '$L_t$'
# a = lr ; xlabel = '$L_r$'
# a = radii ; xlabel = '$R_0$'

# a = [1/i**2 for i in a] ; xlabel = '$Oh^{-2}$'

# a = [(i/j) for i, j in zip(lt, lv)]; xlabel = '$L_v/L_T$'
# a = [(i/j) for i, j in zip(lr, lv)]; xlabel = '$L_r/L_T$'
# a = [r/(i) for i,r in zip(lt,radii)]; xlabel = '$R_0/L_T$'
# a = [r/(i) for i,r in zip(lv,radii)]; xlabel = '$R_0/L_v$'
# a = [r/(i) for i,r in zip(lr,radii)]; xlabel = '$R_0/L_r$'

a = [((i/r)**.5*(j/r)**1)**1 for r, i, j in zip(radii, lv, lt)]; xlabel = '$Oh Th$'

# a = [(r*p)/(i*j) for r,p,  i, j in zip(radii,  lr, lv, lt)] ; xlabel = '$RL_T/L_pL_v$'
# a = [r**2/(i*j) for r, i, j in zip(radii, lv, lt)]; xlabel = '$R_0^{2}/L_vL_T$'
# a = [(r**2/(i*j))**-1 for r, i, j in zip(radii, lv, lt)]; xlabel = r'$ {L_vL_T}/{R_0^2} = Oh^2Th $'
# a = [(r**2/(i*j))**-0.5 for r, i, j in zip(radii, lv, lt)]; xlabel = '$\sqrt{L_vL_T}/R_0$'
# a = [((i*j/r**2))**0.5 for r, i, j in zip(radii, lv, lt)]; xlabel = '$L_vL_T/R_0^2$'
# a = [(r**3/(i*j*p))**-1 for r, i, j, p in zip(radii, lv, lt, lr)]; xlabel = '$R_0/\sqrt[3]{L_vL_TL_r}$'

# a = [(r*x**2/(i*j*p))**0.25 for r, x, i, j, p in zip(radii, wavelen, lv, lt, lr)]; xlabel = '$R_0/\sqrt[3]{L_vL_TL_r}$'
# a = [((j/i)/x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$L_v/\lambda L_T$'
# a = [((j/i)*x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda L_v/ L_T$'
# a = [(x**2/(i*j))**0.5 for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda^2/ L_v L_T$'
# a = [(x) for x, i, j in zip(wave, lv, lt)] ; xlabel = '$1/\lambda $'
# a = [x*(i/j) for x, i, j in zip(red_wavenum, lv, lt)] ; xlabel = '$\chi L_T/L_v$'

# a = [x/i for x, i in zip(wave, lv)] ; xlabel = '$L_v/\lambda$'
# a = [r/x for x, r in zip(wave, radii)]; xlabel = '$R_0/\chi$'

type_plt = ''
# type_plt = 'loglog'
# type_plt = 'semilogx'
# type_plt = 'semilogy'


scale = (max(a[:-end]) - min(a[:-end])) * 0.1
lla = min(a[:-end])
ula = max(a[:-end])
a2 = np.linspace(lla-scale*0.1, ula+scale*1, 100)

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

def fpow(x,a,b):
    return a*x**b

def fexp2(x,a,b,c):
    return c-a*np.exp(x*b)

def flog(x,a,b):
    return a*np.log(x) + b


from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=fpow, xdata=a, ydata=b, p0=[0, 0], bounds=(-np.inf, np.inf))
pars3, cov3 = curve_fit(f=flog, xdata=a, ydata=b, maxfev=10000)
pars4, cov4 = curve_fit(f=fexp2, xdata=a, ydata=b, maxfev=100000)

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
for i, j in enumerate(a):
    print(i,j)
    s1 += (ff1(j)-b[i])**2
    s2 += (ff2(j)-b[i])**2
    s3 += (fexp(j, *pars)-b[i])**2
    s4 += (fpow(j, *pars2)-b[i])**2
    s6 += (flog(j, *pars3)-b[i])**2
    s5 += (fexp2(j, *pars4)-b[i])**2

print(s1, s2, s3, s4, s5, s6)
print(fit, '\n', fit2)
print(pars, stdevs)
print(pars2, stdevs2)
print(pars3, stdevs3)
print(pars4, stdevs4)


import matplotlib as mpl
from matplotlib import container


dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12*2,
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


if type_plt == 'loglog':
    ax2.loglog(a2, fpow(a2, *pars2), 'g--', label='pow')
elif type_plt == 'semilogx':
    ax2.semilogx(a2, fpow(a2, *pars2), 'g--', label='pow')
elif type_plt == 'semilogy':
    ax2.semilogy(a2, fpow(a2, *pars2), 'g--', label='pow')
else:
    ax2.plot(a2, fpow(a2, *pars2), 'g--', label='pow')

yerr = np.sqrt(b_var[:-end])*1

# ax2.loglog(a2, b_fit, 'k--', label='Linear fit')
# ax2.plot(a2, b_fit2, 'k--', label='Quadratic fit')
# ax2.plot(a2, fexp(a2, *pars), 'r--', label='exp ')
# ax2.plot(a2, flog(a2, *pars3), 'b--', label='Log Fit')
# ax2.plot(a2, fexp2(a2, *pars4), 'y--', label='exp2')
# ax2.plot(a2, fpow(a2, *pars2), 'g--', label='pow')
# ax2.plot(a, b, 'ko', label='Simulation')
ax2.errorbar(a[:-end], b[:-end], yerr = yerr,
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc=0, ncol=1)
ax2.set_ylabel('$N_{satellite}/N_{main}$')
ax2.set_xlabel(xlabel)
# ax2.set_xlabel(r'$3R_0/l_T$')



# plt.savefig('fig4.pdf', bbox_inches='tight', dpi=dpi )


plt.show()
