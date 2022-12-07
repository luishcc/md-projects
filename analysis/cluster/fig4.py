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

a=wave
fit = np.polyfit(a,b, 1)
scale = (a[-1] - a[0]) * 0.1
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


#############################
#############################


# aa = [50,60,70,80,85,90]
aa = [0.266, .321, .451, .704, .901, 1.137]

# Main droplet break_avg
bb = [9.545, 9.589, 9.923, 10.649, 10.969, 11.335]
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

ax1.errorbar(wave, bb, xerr = np.sqrt(q_var)*2*np.pi*4.8,
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
ax1.legend(handles, labels, loc='lower left', ncol=1)



# ax2.plot(a2, b_fit, 'k--', label='Linear fit')
# ax2.plot(a2, b_fit2, 'k--', label='Quadratic fit')
# ax2.plot(a2, fexp(a2, *pars), 'b--', label='exp fit')
# ax2.plot(a2, fpow(a2, *pars2), 'k--', label='$y=0.13x^{-0.5}$')
# ax2.plot(a, b, 'ko', label='Simulation')
# ax2.errorbar(a, b, yerr = np.sqrt(b_var),
# fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
ax2.errorbar(wave, b, xerr = np.sqrt(q_var)*2*np.pi*4.8, yerr = np.sqrt(b_var),
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc=0, ncol=1)
ax2.set_ylabel('$N_{satellite}/N_{total}$')
ax2.set_xlabel('Oh')



# plt.savefig('fig4.pdf', bbox_inches='tight', dpi=dpi )


plt.show()
