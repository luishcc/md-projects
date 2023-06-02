from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
# from mdpkg.rwfile import read_dat


path_to_data = '/home/luishcc/hdd/free_thread_old/'
path_to_data = '/home/luishcc/hdd/surfactant/'
path_to_data = '/home/luishcc/hdd/surfactant/new/'
# path_to_data = '/home/luishcc/hdd/free_thread_new/'
# path_to_data = '/home/luishcc/hdd/'


def get_snap(dir, exact=True):
    try:
        with open(dir+'/breaktime.txt', 'r') as fd:
            snap = int(fd.readline())
    except:
        return None
    return snap

R = 8
ratio = 48
A = 90

surf_con = 2.0


grid = 1

ini = 1
end = 14


# data_case_dir = f'R{R}_ratio{ratio}_A{A}/1'
data_case_dir = f'R{R}-{surf_con}/1'
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
    popt, pcov = opt.curve_fit(gaus, xx2, value[ini:end],
                p0=[1,mean, sigma], maxfev=100000)

    return xxx[np.argmax(gaus(xxx,*popt))], (xxx, gaus(xxx, *popt))

#############################################

num = [i+1 for i in range(20)]


n = 1
peak = []
avg_lst = []
var_lst = []
peak_sum = 0
peak_sum2 = 0
# while os.path.isfile(datafile):
import random
while True:
    try:
        nn = num.pop(random.randrange(len(num)))
        print(nn)
    except:
        print('Error \n\n')
        break
    print(snap)
    print(datafile)
    data = pd.read_csv(datafile, sep=' ', header=0, names=['dz', 'correlation', 'nan'])
    # data = pd.read_dat(datafile)

    arr_real = np.array(data['correlation'].tolist())
    arr = abs(rfft(arr_real))
    ar_lst = arr.tolist()
    #
    # xx_l = xx.tolist()
    # p_fit = xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # ar_lst.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit += xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # ar_lst.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit += xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # ar_lst.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit += xx_l.pop(np.argmax(ar_lst[ini:])+ini)
    # p_fit /= 3

    p_fit, plot = fit(arr)
    # p_fit, plot = fit2(arr)

    print(p_fit)

    peak.append(p_fit)
    peak_sum += p_fit
    peak_sum2 += p_fit**2
    sum += arr
    sumsq += arr**2
    n += 1

    if n > 2:
        avg2 = peak_sum/(n-1)
        var2 = 0
        for aa in peak:
            var2 += (aa - avg2)**2
        avg_lst.append(avg2)
        var_lst.append((var2/(len(peak)-1))/(n-1))

    # data_case_dir = f'R{R}_ratio{ratio}_A{A}/{nn}'
    data_case_dir = f'R{R}-{surf_con}/{nn}'

    dir = path_to_data + data_case_dir
    datafile = '/'.join([dir,file])
    snap = get_snap(dir)

avg = sum/(n-1)
var = sumsq/(n-1) - avg**2

peak_avg = peak_sum/(n-1)
peak_var = peak_sum2/(n-1) - peak_avg**2



fig, ax = plt.subplots(1,1)

x = np.linspace(1,n-1,n-1-1)

ax.errorbar(x[1:], avg_lst[1:], yerr =[i**.5 for i in var_lst[1:]], fmt='o', ecolor = 'black', markersize=3.5, color='black', capsize= 3, capthick=1)

plt.show()
