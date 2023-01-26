import numpy as np

# aa = [50,60,70,80,85,90]
aa = [0.266, .321, .451, .704, .901, 1.137]

# Main droplet break_avg
bb = [9.545, 9.589, 9.923, 10.649, 10.969, 11.335]
bb = [i/4.8 for i in bb]

bb2 =[3.48, 3.39, 3.38, 3.43, 3.98, 3.8, 4.2]
bb2 = [i/1.6 for i in bb2]

bb4 =[6.32, 5.8, 6.03, 6.14, 6.35, 6.97, 6.9]
bb4 = [i/3.2 for i in bb4]

cc = [1.248, 1.151, 1.234, 1.109, 1.222, .932]

# Main droplet break_avg_peak
# bb = [10.064, 10.136, 10.647, 11.33, 11.606, 11.765]
# cc2 = [1.42, 1.42, 1.4, 1.24, 1.14, 1.02]
#
# # Main droplet normal_avg
# bb = [9.547, 9.641, 10.042, 10.722, 10.819, 11.4]
# cc3 = [1.278, 1.111, 1.234, 1.12, 1.322, .876]


Rr = [2,4,6]
A=[40,50,60,70,80,85,90]
ratio=48
q = {}
qinv = {}
q_var = {}
for r in Rr:
    q[r]=[]
    qinv[r]=[]
    q_var[r]=[]
    for a in A:
        file = f'/home/luishcc/md-projects/analysis/density_correlation/peak/R{r}_ratio{ratio}_A{a}-peak.csv'
        try:
            with open(file, 'r') as fd:
                fd.readline()
                line = fd.readline().split(',')
                q[r].append(float(line[0]) * 2 * np.pi * r*0.8)
                qinv[r].append(1/(float(line[0]) * r*0.8))
                q_var[r].append(float(line[1]) * ( 2 * np.pi * r*0.8)**2)
        except Exception as e:
            print(e)
            continue

wave = [.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]

wave = [i*2*np.pi*4.8 for i in wave]

q_var6 = [3.156327982930347e-06,
2.328394395880221e-06,
1.8893985765694086e-06,
2.054396275751638e-06,
3.954677744054939e-06,
9.193559899539904e-06]



# q_var = [i*2*np.pi*4.8 for i in q_var]

aa = wave
# ffit = np.polyfit(aa,bb, 1)
# bb_fit = [fit[0]*i + fit[1] for i in aa ]
#
dda = (aa[1]-aa[0])*0.3
a2 = np.linspace(aa[0]-dda, aa[-1]+dda, 100)
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
    return np.cbrt(1.5*np.pi/x)


def fexp(x,a,b):
    return a*np.exp(x*b)

def fpow(x,a,b):
    return a*x**b

from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=aa, ydata=bb, p0=[0, 0], bounds=(-np.inf, np.inf))
pars2, cov2 = curve_fit(f=fpow, xdata=aa, ydata=bb, p0=[0, 0], bounds=(-np.inf, np.inf))

stdevs = np.sqrt(np.diag(cov))
stdevs2 = np.sqrt(np.diag(cov2))

s3 = 0
s4 = 0
for i, j in enumerate(aa):
    print(i,j)
    s3 += (fexp(j, *pars)-bb[i])**2
    s4 += (fpow(j, *pars2)-bb[i])**2

print(s3, s4)
print(pars, stdevs)
print(pars2, stdevs2)


import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(ncols=1, nrows=1)

ax1.errorbar(wave, bb, xerr = np.sqrt(q_var6)*2*np.pi*4.8,markerfacecolor='none',
fmt='o',ecolor = 'blue', capsize= 2, capthick=1,color='blue', label=r'$R_0=6$')

ax1.errorbar(q[2], bb2, xerr = np.sqrt(q_var[2]),markerfacecolor='none',
fmt='s',ecolor = 'red', capsize= 2, capthick=1,color='red', label=r'$R_0=2$')

ax1.errorbar(q[4], bb4, xerr = np.sqrt(q_var[4]),markerfacecolor='none',
fmt='x',ecolor = 'green', capsize= 2, capthick=1,color='green', label=r'$R_0=4$')

dv = abs(wave[-1]-wave[0])
pdv = 1 * dv
x = np.linspace(wave[0]+1.4*pdv, wave[-1]-pdv, 100)
ax1.plot(x, pred4(x), 'k--', label='Theory')

# ax1.plot(a2, fpow(a2, *pars2), 'b-', label='$y=7x^{-0.5}$')

ax1.set_xlabel('$\chi$')
ax1.set_ylabel('$R_D/R_0$')
from matplotlib import container
handles, labels = ax1.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax1.legend(handles, labels, loc=0, ncol=1)


# plt.savefig(f'sat_50.png', transparent=True, dpi=1600)

plt.show()
