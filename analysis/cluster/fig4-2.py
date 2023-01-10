import numpy as np




################################################################################
################################################################################
end = 1

a = [.329, .233, .165,
     .538, .380, .311,          # A=-50 new W_p
     .621, .439, .359, .311,    # A=-60 new W_p
     .864, .611,                # A=-70 new W_p
     1.32, .933,                # A=-80 new W_p
     1.66, 1.18,                # A=-85 new W_p
     2.01, 1.42,                # A=-90 new W_p
     .206, .230, .266, .321, .451, .704, .901, 1.137]; xlabel = '$Oh$'

# normal avg
# Different peaks
# b = [.044, .145, .285,
#      .074, .160, .283,
#      .046, .139, .220, .283,
#      .049, .133,
#      .026, .110,
#      .038, .095,
#      .000, .060,
#      .413, .400, .296, .215, .210, .196, .135, .130] # sat/total


# Break_avg
# Different peaks
b = [.046, .145, .279,
     .069, .179, .277,
     .046, .142, .229, .271,
     .049, .137,
     .026, .106,
     .038, .093,
     .0,   .077,
     .411, .402, .282, .213, .200, .181, .126, .133] # sat/total

b_var = [.003, .005, .007,
         .003, .005, .006,
         .002, .007, .006, .006,
         .003, .004,
         .001, .004,
         .004, .003,
         .000, .007,
         .004, .006, .005, .003, .004, .006, .003, .006]


wave = [.1, .1, .1,
        .1, .1, .1,
        .1, .1, .1, .1,
        .1, .1,
        .1, .1,
        .1, .1,
        .1, .1,
.011887547350585061, .01338236354459586,
.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]

radii = [2, 4, 8,
         2, 4, 6,
         2, 4, 6, 8,
         2, 4,
         2, 4,
         2, 4,
         2, 4,
         10, 8, 6, 6, 6, 6, 6, 6]
# radii = [r*0.8 for r in radii]

wavelen = [1/i for i in wave]
red_wavenum = [i*2*np.pi*r for i,r in zip(wave,radii)]


lt = [.356, .356, .356,
      .277, .277, .277,
      .227, .227, .227, .227,
      .193, .193,
      .166, .166,
      .154, .154,
      .145, .145,
      .250, .250, .250, .210, .181, .158, .148, .139]

lv = [.217, .217, .217,
      .581, .581, .581,
      .773, .773, .773, .773,
      1.499, 1.499,
      3.484, 3.484,
      5.545, 5.545,
      8.839, 8.839,
      .426, .426, .426, .617, 1.224, 2.97, 4.87, 7.75]
# lv = [4.8/i for i in lv]

rho = [6.0, 6.0, 6.0,
       6.95, 6.95, 6.95,
       7.7, 7.7, 7.7, 7.7,
       8.4, 8.4,
       9.1, 9.1,
       9.5, 9.5,
       9.8, 9.8,
       7.65, 7.65, 7.65, 8.30, 8.95, 9.6, 9.92, 10.24]
lr = [np.cbrt(1/i) for i in rho]


q_var = [0, 0, 0,
         0, 0, 0,
         0, 0, 0, 0,
         0, 0,
         0, 0,
         0, 0,
         0, 0,
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
# a = [(r**3/(i*j*p))**1 for r, i, j, p in zip(radii, lv, lt, lr)]; xlabel = '$R_0/\sqrt[3]{L_vL_TL_r}$'

# a = [(r*x**2/(i*j*p))**0.25 for r, x, i, j, p in zip(radii, wavelen, lv, lt, lr)]; xlabel = '$R_0/\sqrt[3]{L_vL_TL_r}$'
# a = [((j/i)/x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$L_v/\lambda L_T$'
# a = [((j/i)*x) for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda L_v/ L_T$'
# a = [(x**2/(i*j))**0.5 for x, i, j in zip(wavelen, lv, lt)] ; xlabel = '$\lambda^2/ L_v L_T$'
# a = [(x) for x, i, j in zip(wave, lv, lt)] ; xlabel = '$1/\lambda $'
# a = [x*(i/j) for x, i, j in zip(red_wavenum, lv, lt)] ; xlabel = '$\chi L_T/L_v$'

# a = [x/i for x, i in zip(wave, lv)] ; xlabel = '$L_v/\lambda$'
# a = [r/x for x, r in zip(wave, radii)]; xlabel = '$R_0/\chi$'


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


#############################
#############################


# aa = [50,60,70,80,85,90]
aa = [0.266, .321, .451, .704, .901, 1.137]

# Main droplet break_avg
# bb = [9.545, 9.589, 9.923, 10.649, 10.969, 11.335]

cc = [1.248, 1.151, 1.234, 1.109, 1.222, .932]

# Main droplet break_avg_peak
# bb2 = [10.064, 10.136, 10.647, 11.33, 11.606, 11.765]
# cc2 = [1.42, 1.42, 1.4, 1.24, 1.14, 1.02]
#
# # Main droplet normal_avg
bb = [9.547, 9.741, 10.042, 10.722, 10.819, 11.4]
# cc3 = [1.278, 1.111, 1.234, 1.12, 1.322, .876]


wave = [.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]
# wave = [1/i for i in wave]
wave = [i*2*np.pi*4.8 for i in wave]

q_var = [3.156327982930347e-06,
2.328394395880221e-06,
1.8893985765694086e-06,
2.054396275751638e-06,
3.954677744054939e-06,
9.193559899539904e-06]
# q_var = [i*2*np.pi*4.8 for i in q_var]


# ffit = np.polyfit(aa,bb, 1)
# bb_fit = [fit[0]*i + fit[1] for i in aa ]
#
# aa2 = np.linspace(aa[0], aa[-1], 100)
# ffit2 = np.polyfit(aa, bb, 2)
# bb_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in aa2 ]


def pred(x):
    scale = 0.8
    return np.cbrt(0.75*(6*scale)**2*x-1.2**3)
    # return np.cbrt(0.75*(6*1)**2*x-8.6**3)

def pred2(x):
    scale = 1.012
    return 0.75*(6*scale)**2*x-8.7**3

def pred3(x):
    scale = 0.8
    return np.cbrt(0.75*(6*scale)**2/x)

def pred4(x):
    scale = 0.8
    return (6*scale)*np.cbrt(1.5*np.pi/x)


##########################################
##########################################


import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 1.1*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt

fig, axs = plt.subplots(ncols=1, nrows=3)
# gs = axs[0, 0].get_gridspec()
# for ax in axs[0, :]:
#     ax.remove()
# axbig = fig.add_subplot(gs[0, :])

fig.subplots_adjust(hspace=.4)
fig.subplots_adjust(wspace=.4)

# fig.tight_layout()

ax0 = axs[0]
ax1 = axs[1]
ax2 = axs[2]

##########################################
import pandas as pd

R = 6
ratio = 48
A = -50
snap = 100

# file = f'~/md-projects/analysis/cluster/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'
file = f'~/md-projects/analysis/cluster/break-avg/R{R}_ratio{ratio}_A{abs(A)}/{snap}.csv'

df = pd.read_csv(file)
df.drop(df[df['size'] <= 3].index, inplace=True)
df.drop(df[df['anisotropy'] > 0.2].index, inplace=True)
df['radius'] = df['radius'].multiply(np.sqrt(5/3))
df['radius'].plot.hist(bins=100, alpha=0.4, ax=ax0, density=True, color='b')
df['radius'].plot.kde(bw_method=0.1, ax=ax0, color='k')
ax0.set_xlim(0,16)
ax0.set_xlabel('$R_D$')
ax0.set_ylabel('Distribution Density')
ax0.annotate('', xy=(2.8, 0.13), xytext=(1.6,0.12),
            arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
            )
ax0.annotate('', xy=(6.4,0.28), xytext=(8.76,0.26),
            arrowprops=dict(facecolor='black', lw=1.5, arrowstyle='<-'),
            )
ax0.annotate('Main Droplets', xy=(3.5, 0.3))
ax0.annotate('Satellite Droplets', xy=(3, 0.12))

##########################################

ax1.errorbar(wave, bb, xerr = np.sqrt(q_var)*2*np.pi*4.8, markerfacecolor='none',
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
dv = abs(wave[-1]-wave[0])
pdv = 0.3 * dv
x = np.linspace(wave[0]+pdv, wave[-1]-pdv, 100)
ax1.plot(x, pred4(x), 'k--', label='Theory')
ax1.set_xlabel('$\chi$')
ax1.set_ylabel('$R_D$')
from matplotlib import container
handles, labels = ax1.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax1.legend(handles, labels, loc='lower left', ncol=1, frameon=False)



# ax2.plot(a2, b_fit, 'k--', label='Linear fit')
# ax2.plot(a2, b_fit2, 'k--', label='Quadratic fit')
# ax2.plot(a2, fexp(a2, *pars), 'b--', label='exp fit')
# ax2.loglog(a2, flog(a2, *pars3), 'k--', label='Log Fit')
ax2.semilogx(a2, fpow(a2, *pars2), 'k--', label='Power Law')
# ax2.plot(a, b, 'ko', label='Simulation')
# ax2.errorbar(a, b, yerr = np.sqrt(b_var),
# fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
ax2.errorbar(a, b, yerr = np.sqrt(b_var),
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation', markerfacecolor='none')
handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc=0, ncol=1, frameon=False)
ax2.set_ylabel('$N_{satellite}/N_{main}$')
ax2.set_xlabel(xlabel)



# plt.savefig('fig4.pdf', bbox_inches='tight', dpi=dpi )


plt.show()
