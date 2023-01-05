import numpy as np
import matplotlib.pyplot as plt

x = [-50, -60, -70, -80, -90]
y = [7.22, 10.76, 18.31, 33.90, 64.01]


fit = np.polyfit(x,y,2)
def ff2(a):
    return fit[0]*a**2 + fit[1]*a +fit[2]

def fexp(x,a,b):
    return a*np.exp(x*b)

from scipy.optimize import curve_fit
pars, cov = curve_fit(f=fexp, xdata=x, ydata=y, p0=[0, 0], bounds=(-np.inf, np.inf))

x2 = np.linspace(min(x)-10, max(x)+10, 100)
y_fit = [fit[0]*i**2 + fit[1]*i +fit[2] for i in x2 ]

fig, ax = plt.subplots(1,1)

ax.plot(x,y, 'ko')
# ax.plot(x2, y_fit, 'b--')
ax.plot(x2, fexp(x2, *pars), 'r--')

print(fexp(-40, *pars))

plt.show()
