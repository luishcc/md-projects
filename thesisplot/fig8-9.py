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
     .069, .160, .250, #.179, .277,
     .046, .142, .229, .271,
     .049, .137,
     .026, .106,
     .038, .093,
     .000,   .077,
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

a = [((i/r)**.5*(j/r)**1)**1 for r, i, j in zip(radii, lv, lt)]; xlabel = 'OhTh'
# a = [((i/r)**.6*(j/r)**1)**1 for r, i, j in zip(radii, lv, lt)]; xlabel = 'OhTh'


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
    return np.cbrt(1.5*np.pi/x)


##########################################
##########################################


import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 15,
    'figure.figsize': (1.1*side, .6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
from matplotlib import container


fig, axs = plt.subplots(ncols=1, nrows=1)
fig2, axs2 = plt.subplots(ncols=1, nrows=1)


fig.subplots_adjust(hspace=.4)
# fig.subplots_adjust(wspace=.4)

# fig.tight_layout()

ax1 = axs
ax2 = axs2

ax22 = plt.axes([0,0,1,1])
ip = InsetPosition(ax2, [0.5,0.4,0.45,0.5])
ax22.set_axes_locator(ip)

##########################################
# scale_r = {2:.8, 4:.8, 6:.8}
scale_r = {2:.85, 4:.85, 6:.8}

radii_r = {2:[1.55, 1.5, 1.45, 1.41, 1.39, 1.36, 1.3],
           4:[3.2, 3.1, 3, 3, 2.9, 2.85, 2.8],
           6:[5.3, 5, 4.8, 4.5, 4.4, 4.35, 4.3]}

# Main droplet break_avg
bbb = [9.78, 9.62, 9.55, 9.923, 10.649, 10.969, 11.335]
bbb = [10.2, 9.9, 10, 10.7, 11.2, 11.6, 11.9]
bbb = [i/(ri) for i,ri in zip(bbb, radii_r[6])]

# bbb2 =[3.48, 3.39, 3.38, 3.43, 3.98, 3.8, 4.2]
bbb2 =[3.60, 3.63, 3.70, 3.77, 3.88, 4.01, 4.6]
bbb2 = [i/(ri) for i,ri in zip(bbb2, radii_r[2])]

bbb4 =[7.08, 6.9, 7.1, 7.5, 7.9, 7.9, 8.5]
bbb4 = [i/(ri) for i,ri in zip(bbb4, radii_r[4])]


Rr = [2,4,6]
A=[40,50,60,70,80,85,90]


ratio=48
qq = {}
qqinv = {}
qq_var = {}
for r in Rr:
    qq[r]=[]
    qqinv[r]=[]
    qq_var[r]=[]
    for i,av in enumerate(A):
        file = f'/home/luishcc/md-projects/analysis/density_correlation/peak/R{r}_ratio{ratio}_A{av}-peak.csv'
        try:
            with open(file, 'r') as fd:
                fd.readline()
                line = fd.readline().split(',')                
                qq[r].append(float(line[0]) * 2 * np.pi * radii_r[r][i])
                qqinv[r].append(1/(float(line[0]) * radii_r[r][i]))
                qq_var[r].append(float(line[1]) * ( 2 * np.pi * radii_r[r][i])**2)
        except Exception as e:
            print(e)
            continue

wwave = [.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]

wwave = [i*2*np.pi*4.8 for i in wwave]

q_var6 = [3.156327982930347e-06,
2.328394395880221e-06,
1.8893985765694086e-06,
2.054396275751638e-06,
3.954677744054939e-06,
9.193559899539904e-06]

def pred4(x):
    return np.cbrt(1.5*np.pi/x)


ax1.errorbar(qq[6], bbb, xerr = 2*np.sqrt(np.array(qq_var[6])/20),markerfacecolor='none',
fmt='none',ecolor = 'blue', capsize=5, capthick=2,color='blue')
ax1.scatter(qq[6], bbb, c='none',
marker='o', edgecolor = 'blue', s=60, label=r'$R_0=6$', linewidth=2)

ax1.errorbar(qq[2], bbb2, xerr = 2*np.sqrt(np.array(qq_var[2])/20),markerfacecolor='none',
fmt='none',ecolor = 'red', capsize= 5, capthick=2,color='red')
ax1.scatter(qq[2], bbb2, c='none',
marker='s', edgecolor = 'red', s=60, label=r'$R_0=2$', linewidth=2)

ax1.errorbar(qq[4], bbb4, xerr = 2*np.sqrt(np.array(qq_var[4])/20),
fmt='none',ecolor = 'green', capsize=5, capthick=2,color='green')
ax1.scatter(qq[4], bbb4, c='none',
marker='^', edgecolor = 'green', s=60, label=r'$R_0=4$', linewidth=2)

all_bbb = bbb + bbb2 + bbb4
all_qq = qq[6] + qq[2] + qq[4]

# pars, cov = curve_fit(f=fexp, xdata=all_qq, ydata=all_bbb, p0=[0, 0], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=fpow, xdata=all_qq, ydata=all_bbb, p0=[0, 0], bounds=(-np.inf, np.inf))
# pars3, cov3 = curve_fit(f=flog, xdata=all_qq, ydata=all_bbb, maxfev=10000)
# pars4, cov4 = curve_fit(f=fexp2, xdata=all_qq, ydata=all_bbb, maxfev=100000)

stdevs = np.sqrt(np.diag(cov))
stdevs2 = np.sqrt(np.diag(cov2))
stdevs3 = np.sqrt(np.diag(cov3))
stdevs4 = np.sqrt(np.diag(cov4))

s3 = 0
s4 = 0
s5 = 0
s6 = 0
for i, j in enumerate(all_qq):
    print(i,j)
    s3 += (fexp(j, *pars)-all_bbb[i])**2
    s4 += (fpow(j, *pars2)-all_bbb[i])**2
    s6 += (flog(j, *pars3)-all_bbb[i])**2
    s5 += (fexp2(j, *pars4)-all_bbb[i])**2

print("FIT \n")
print(s3, s4, s5, s6)
print(pars, stdevs)
print(pars2, stdevs2)
print(pars3, stdevs3)
print(pars4, stdevs4)


#######

dv = abs(qq[6][-1]-qq[6][0])
pdv = 1.2 * dv
x = np.linspace(wwave[0]+1.*pdv, wwave[-1]-pdv, 100)
ax1.plot(x, pred4(x), 'k--', label='Theory',
         linewidth=2.5)

ax1.plot(x, fpow(x, *pars2), 'b-.', 
         label=r'$R_D/R_0 \sim \chi^{-0.62}$ (Fit)',
         linewidth=2.5)


ax1.set_xlabel('$\chi$')
ax1.set_ylabel('$R_D/R_0$')
ax1.set_xlim(0.17, 0.7 )
ax1.set_ylim(1.8, 3.11)

from matplotlib import container
handles, labels = ax1.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
first_legend = ax1.legend(handles[3:], labels[3:], loc='lower left', ncol=1, frameon=False)
ax1.add_artist(first_legend)
ax1.legend(handles[:3], labels[:3], loc='upper right', ncol=1, frameon=False)


##########################################

# a = [((i/r)**.5*(j/r)**1)**1 for r, i, j in zip(radii, lv, lt)]; xlabel = 'OhTh'
# ax2.plot(a2, b_fit, 'k--', label='Linear fit')
# ax2.plot(a2, b_fit2, 'k--', label='Quadratic fit')
# ax2.plot(a2, fexp(a2, *pars), 'b--', label='exp fit')
# ax2.loglog(a2, flog(a2, *pars3), 'k--', label='Log Fit')
ax2.plot(a2, fpow(a2, *pars2), 'k--', label='Power Law', linewidth=2)
# ax2.plot(a, b, 'ko', label='Simulation')
# ax2.errorbar(a, b, yerr = np.sqrt(b_var),
# fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
ax2.errorbar(a, b, yerr = 2*np.sqrt(np.array(b_var)/20),
    fmt='none',ecolor = 'black', capsize= 4, capthick=2,color='black')
ax2.scatter(a, b, marker='o', edgecolor = 'black', 
    c = 'none', linewidth=2, s=60, label='Simulation')
ax2.set_ylabel('$N_{satellite}/N_{total}$')
ax2.set_xlabel(xlabel)

handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc=(.13, .75), ncol=1, frameon=False)

from matplotlib.patches import Polygon

ax22.set_ylim(1e-2, 7e-1)
ax22.loglog(a2, fpow(a2, *pars2), 'k--', label='Power Law', linewidth=2)
ax22.scatter(a, b, marker='o',color = 'black', facecolors='none', 
             label='Simulation', linewidth=2)
t1 = Polygon([[.022, .03], [.022, .06], [.06, .03]], facecolor='none', edgecolor='black')
ax22.add_patch(t1)
ax22.annotate(r'$0.72\pm0.04$', xy=(.0036, 0.035), fontsize=15)



fig.savefig('ch3size.pdf', bbox_inches='tight', dpi=dpi )
# fig2.savefig('ch3sat.pdf', bbox_inches='tight', dpi=dpi )




plt.show()
