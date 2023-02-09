from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
# from mdpkg.rwfile import read_dat


path_to_data = '/home/luishcc/hdd/free_thread_old/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
# path_to_data = '/home/luishcc/hdd/'


def get_snap(dir, exact=True):
    try:
        with open(dir+'/breaktime.txt', 'r') as fd:
            snap = int(fd.readline())
    except:
        return None
    return snap

R = 6
ratio = 48
A = 90

grid = 1

ini = 1
end = 30


data_case_dir = f'R{R}_ratio{ratio}_A{A}/1'
dir = path_to_data + data_case_dir

snap = get_snap(dir)

file = f'breaktime_correlation_grid{grid}.dat'
datafile = '/'.join([dir,file])

data = pd.read_csv(datafile,  sep=' ', header=0, names=['dz', 'correlation', 'nan'])
x = data['dz'].tolist()

num = len(x)
if num % 2 == 0:
    row = int((num / 2) + 1)
else:
    row = int((num + 1) / 2)

xx = rfftfreq(num)

sum = np.zeros(row)
sumsq = np.zeros(row)

###############

############

from scipy.interpolate import interp1d, splrep, splev, CubicSpline
import scipy.optimize as opt
from numpy import asarray as ar,exp
from scipy.stats import chisquare
from scipy import stats

initials = [8, 20, 5 , -10] # initial guess
from scipy.optimize import leastsq
from scipy.special import erf

def asymGaussian(x, p):
    amp = (p[0] / (p[2] * np.sqrt(2 * np.pi)))
    spread = np.exp((-(x - p[1]) ** 2.0) / (2 * p[2] ** 2.0))
    skew = (1 + erf((p[3] * (x - p[1])) / (p[2] * np.sqrt(2))))
    return amp * spread * skew

def residuals(p,y,x):
    return y - asymGaussian(x, p)

def fit2(value):
    xx2 = xx[ini:end]
    xxx = np.linspace(xx2[0], xx2[-1], 300)

    cnsts = leastsq(residuals, initials, maxfev=100000,
                    args=(value[ini:end], # y value
                          xx2  # x value
                          ))[0]

    gaussk = asymGaussian(xxx, cnsts)

    return xxx[np.argmax(gaussk)], (xxx, gaussk)

###################
def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))

from numpy import asarray as ar,exp
import scipy.optimize as opt

def fit(value):
    xx2 = xx[ini:end]
    xxx = np.linspace(xx2[0], xx2[-1], 300)

    nn = len(xx2)
    mean = ((xx2)*(value[ini:end]))/nn
    mean = mean.sum()
    sigma = ((value[ini:end])*((xx2)-mean)**2)/nn
    sigma = sigma.sum()
    popt, pcov = opt.curve_fit(gaus, xx2, value[ini:end], p0=[1,mean, sigma], maxfev=10000)

    return xxx[np.argmax(gaus(xxx,*popt))], (xxx, gaus(xxx, *popt))

#############################################


n = 1
peak = []
peak_sum = 0
peak_sum2 = 0
while os.path.isfile(datafile):
    print(snap)
    print(datafile)
    data = pd.read_csv(datafile, sep=' ', header=0, names=['dz', 'correlation', 'nan'])
    # data = pd.read_dat(datafile)

    arr_real = np.array(data['correlation'].tolist())
    arr = abs(rfft(arr_real))
    ar_lst = arr.tolist()
    #
    xx_l = xx.tolist()
    # p_fit = xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # ar_lst.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit += xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # ar_lst.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit += xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # ar_lst.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit += xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit /= 3

    p_fit, plot = fit(arr)
    # p_fit, plot = fit2(a  rr)

    print(p_fit)
    # plt.figure(1)
    # plt.plot(xx[1:], arr[1:])
    # plt.plot(*plot)
    # plt.xlim(0, 0.1)
    # plt.show()
    # plt.clf()

    peak.append(p_fit)
    peak_sum += p_fit
    peak_sum2 += p_fit**2
    sum += arr
    sumsq += arr**2
    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{A}/{n}'
    dir = path_to_data + data_case_dir
    datafile = '/'.join([dir,file])
    snap = get_snap(dir)


avg = sum/(n-1)
var = sumsq/(n-1) - avg**2

peak_avg = peak_sum/(n-1)
peak_var = peak_sum2/(n-1) - peak_avg**2


xx2 = xx[ini:end]
xxx = np.linspace(xx2[0], xx2[-1], 300)



# print(peak_avg, np.sqrt(peak_var), peak_var)
# with open(f'R{R}_ratio{ratio}_A{A}-peak.csv', 'w') as fd:
#     fd.write('peak_avg,variance\n')
#     fd.write(f'{peak_avg},{peak_var}')

from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
xx2 = xx[ini:end]
xxx = np.linspace(xx2[0], xx2[-1], 300)

fig, ax = plt.subplots(1,1)

ax1 = plt.axes([0,0,1,1])
ip = InsetPosition(ax, [0.55,0.35,0.42,0.6])
ax1.set_axes_locator(ip)
mark_inset(ax, ax1, loc1=2, loc2=4, fc="none", ec='0.3')


ax.plot(xx[1:],avg[1:], 'k-', linewidth=1.5)
ax.errorbar(xx[1:], avg[1:], yerr = np.sqrt(var[1:])/2, fmt='o',ecolor = 'black',markersize=3.5, color='black', capsize= 3, capthick=1)
ax.errorbar(peak_avg, 0, xerr = np.sqrt(peak_var)/2, fmt='o',ecolor = 'black',markersize=3.5, color='black', capsize= 3, capthick=1)

ax.set_xlim(0,0.1)

ax.set_title(f'A={-A}')
ax.set_ylabel(r'$\hat{G}(r,q)$')
ax.set_xlabel(r'$q$')
# ax.plot(xxx, gaussk)

# xx2 = xx[ini:end]
# xxx = np.linspace(xx2[0], xx2[-1], 300)
# nn = len(xx2)
# mean = ((xx2)*(avg[ini:end]))/nn
# mean = mean.sum()
# sigma = ((avg[ini:end])*((xx2)-mean)**2)/nn
# sigma = sigma.sum()
# popt, pcov = opt.curve_fit(gaus, xx2, avg[ini:end], p0=[1,mean, sigma], maxfev=10000)
#
# pp, plot = fit2(avg)
#
# print(pp)


nn = len(xx2)
mean = ((xx2)*(avg[ini:end]))/nn
mean = mean.sum()
sigma = ((avg[ini:end])*((xx2)-mean)**2)/nn
sigma = sigma.sum()
popt, pcov = opt.curve_fit(gaus, xx2, avg[ini:end], p0=[1,mean, sigma], maxfev=10000)

# ax1.plot(np.linspace(1,n, len(peak)), peak, 'k.-', linewidth=2.5)


ax1.plot(xx[ini:end],avg[ini:end], 'k--', linewidth=2., label='Data')
ax1.plot(xxx, gaus(xxx, *popt), 'b-', linewidth=2.5, label='gauss')
# ax1.plot(*plot, 'b-', linewidth=2.5, label='gauss')

# ax1.plot(np.linspace(1,n, len(peak)), peak, 'k.-', linewidth=2.5)

plt.show()
#
# with open(f'R{R}_ratio{ratio}_A{A}-peak.csv', 'w') as fd:
#     fd.write('peak_avg,variance\n')
#     fd.write(f'{popt[0]},{popt[1]}')
