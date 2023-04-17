import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.9*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


x = [-40, -50, -60, -70, -80, -85, -90]
y = [6.75, 7.65, 8.3, 8.95, 9.6, 9.92, 10.24]
y2 = [4.06, 7.22, 10.76, 18.31, 33.90, 47.02, 64.01]
y3 = [9.95, 15.90, 22.60, 30.66, 40.29, 45.73, 51.62]
# y = [6.9, 7.7, 8.4, 9.1, 9.8]

#
#
# fit = np.polyfit(x,y,2)
# def ff2(a):
#     return fit[0]*a**2 + fit[1]*a +fit[2]
#
# def fexp(x,a,b):
#     return a*np.exp(x*b)
#
# from scipy.optimize import curve_fit
# pars, cov = curve_fit(f=fexp, xdata=x, ydata=y, p0=[0, 0], bounds=(-np.inf, np.inf))
#
# x2 = np.linspace(min(x)-10, max(x)+10, 100)
# y_fit = [fit[0]*i**2 + fit[1]*i +fit[2] for i in x2 ]

fig, ax = plt.subplots(1,1)

ax.plot(x,y, 'ko-', label=r'$\rho$')
ax.plot(x,y2, 'r<-', label=r'$\mu$')
ax.plot(x,y3, 'bs-', label=r'$\sigma$')

ax.set_xlabel('A')
ax.set_ylabel('Respective DPD unit')

ax.legend(frameon=False)

# ax.plot(x2, y_fit, 'b--')
# ax.plot(x2, fexp(x2, *pars), 'r--')

# print(fexp(-40, *pars))

plt.show()
