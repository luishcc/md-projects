import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, splrep, splev, CubicSpline
import scipy.optimize as opt
from mdpkg.rwfile import read_dat, Dat
from numpy import asarray as ar,exp
from scipy.stats import chisquare
from scipy import stats



R = 6
ratio = 48
A = 80
grid = 1

max = 600
skip = 0


data_case_dir = f'R{R}_ratio{ratio}_A{A}'
path_to_data = '/'.join([os.getcwd(), data_case_dir, f'fourier'])
save_correlation_dir = '/'.join([path_to_data, 'fitting'])

if not os.path.isdir(save_correlation_dir):
    os.mkdir(save_correlation_dir)

snaps = {50: [170],
         60: [180],
         70: [185, 200],
         80: [200],
         85: [215],
         90: [240]}

plt.figure(1)

def func(x, a, b, c, d):
    return a + b*x + c*x*2 + d*x**3


initials = [10, 30, 8 , -15] # initial guess
from scipy.optimize import leastsq
from scipy.special import erf

def asymGaussian(x, p):
    amp = (p[0] / (p[2] * np.sqrt(2 * np.pi)))
    spread = np.exp((-(x - p[1]) ** 2.0) / (2 * p[2] ** 2.0))
    skew = (1 + erf((p[3] * (x - p[1])) / (p[2] * np.sqrt(2))))
    return amp * spread * skew

def residuals(p,y,x):
    return y - asymGaussian(x, p)


for snap in snaps[A]:
    print(snap)
    data = read_dat('/'.join([path_to_data, f'{snap}.dat']))
    # l = len(data['freq'][7:])//6
    x = np.multiply(data['freq'][3:50], 1)
    y = np.multiply(data[str(6)][3:50], 1)
    n = len(x)
    plt.plot(x, y, label=f'time={snap}', marker='.')

    # sa, sloc, sscale = stats.skewnorm.fit(y)
    # sa, sloc, sscale = 10, 0.8, 0.08

    xx = np.linspace(x[0], x[-1], 100)
    # pp = stats.skewnorm.pdf(xx, sa, sloc, sscale)
    # plt.plot(xx, pp, 'k-')

    cnsts = leastsq(residuals, initials,
                    args=(y, # y value
                          x  # x value
                          ))[0]

    gaus = asymGaussian(xx, cnsts)
    gaus2 = asymGaussian(x, cnsts)

    plt.plot(xx,gaus, 'k+')


    ste = np.sqrt( sum( (gaus2 - ar(y))**2 ) /(n-2) )
    chi = sum((gaus2 - ar(y))**2/ar(y))
    chi2 = sum((gaus2 - ar(y))**2/gaus2)
    a = chisquare(y, gaus2)

    print(ste, chi/n, chi2/n )
    print(a[0]/(n-1), a[0], a[1])
    print(xx[np.argmax(gaus)])
    # print(opt.fmin(lambda x1: -gaus(x1,*popt), 0))



# plt.legend()
plt.show()
