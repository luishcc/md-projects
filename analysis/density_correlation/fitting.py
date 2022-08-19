import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, splrep, splev, CubicSpline
import scipy.optimize as opt
from mdpkg.rwfile import read_dat, Dat
from numpy import asarray as ar,exp
from scipy.stats import chisquare


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

def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))

for snap in snaps[A]:
    print(snap)
    data = read_dat('/'.join([path_to_data, f'{snap}.dat']))
    l = len(data['freq'][7:])//6
    x = data['freq'][6:18]
    y = data[str(6)][6:18]
    n = len(x)
    plt.plot(x, y, label=f'time={snap}', marker='.')

    xx = np.linspace(x[0], x[-1], 1000)

    # f = interp1d(x,y, kind='quadratic')
    # # plt.plot(xx, f(xx), 'k--')
    # tck = splrep(x, y, s=None, k=4)
    # plt.plot(xx, splev(xx, tck), 'k--')
    # ste = np.sqrt( sum((splev(x, tck) - ar(y))**2)/(n-2))
    # chi = sum((splev(x, tck) - ar(y))**2/ar(y))
    # chi2 = sum((splev(x, tck) - ar(y))**2/splev(x, tck))

    # x0 = np.array([1.0, 1.0, 1.0, 1.0 ])
    # sigma = np.array([1.0,1.0,1.0,1.0,1.0,1.0])
    # curve = opt.curve_fit(func, x, y, x0, sigma=None)
    # ff = func(xx, curve[0][0], curve[0][1], curve[0][2], curve[0][3])
    # ff2 = ar(func(ar(x), curve[0][0], curve[0][1], curve[0][2], curve[0][3]))
    # plt.plot(xx, ff, 'k--')
    # ste = np.sqrt( sum((ff2 - ar(y))**2)/(n-2))
    # chi = sum((ff2 - ar(y))**2/ar(y))
    # chi2 = sum((ff2 - ar(y))**2/ff2)
    # a = chisquare(y, ff2)
    #
    mean = sum(ar(x)*ar(y))/n
    sigma = sum(ar(y)*(ar(x)-mean)**2)/n
    popt, pcov = opt.curve_fit(gaus, x, y, p0=[1,mean, sigma])
    plt.plot(xx,gaus(xx,*popt),'k--',label='fit')
    ste = np.sqrt( sum((gaus(x,*popt) - ar(y))**2)/(n-2))
    chi = sum((gaus(x,*popt) - ar(y))**2/ar(y))
    chi2 = sum((gaus(x,*popt) - ar(y))**2/gaus(x,*popt))
    # a = chisquare(y, gaus(x,*popt))

    print(ste, chi/n, chi2/n )
    # print(a[0]/(n-1), a[0], a[1])
    print(opt.fmin(lambda x1: -gaus(x1,*popt), 0))



plt.legend()
plt.show()
