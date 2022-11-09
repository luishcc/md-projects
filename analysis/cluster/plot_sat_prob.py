import numpy as np


###############################################################################
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
# b = [.355, .252, .233, .218, .139, .146] # sat/main
b = [.282, .214, .201, .185, .126, .133] # sat/total
# b = [.200, .148, .163, .149, .086, .085] # sat/total
b_var = [.0053, .0026, .0039, .0057, .0025, .0056]
# Main droplet peak
# b = [.205, .151, .163, .152, .088, .093] # sat/total


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
print(pars, stdevs)
print(pars2, stdevs2)


#############################
#############################



import matplotlib as mpl
from matplotlib import container

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

fig, ax2 = plt.subplots(ncols=1, nrows=1)


# ax2.plot(a2, b_fit, 'k--', label='Linear fit')
# ax2.plot(a2, b_fit2, 'k--', label='Quadratic fit')
# ax2.plot(a2, fexp(a2, *pars), 'b--', label='exp fit')
ax2.plot(a2, fpow(a2, *pars2), 'k--', label='$y=0.13x^{-0.5}$')
# ax2.plot(a, b, 'ko', label='Simulation')
ax2.errorbar(a, b, yerr = np.sqrt(b_var),
fmt='o',ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')
handles, labels = ax2.get_legend_handles_labels()
handles = [h[0] if isinstance(h, container.ErrorbarContainer) else h for h in handles]
ax2.legend(handles, labels, loc=0, ncol=1)
ax2.set_ylabel('$N_{satellite}/N_{total}$')
ax2.set_xlabel('Oh')



# plt.savefig('ssa.pdf', bbox_inches='tight', dpi=dpi )


plt.show()
