from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
from mdpkg.rwfile import read_dat
import os
import numpy as np


def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)

A = [50, 60, 70, 80, 85, 90]
oh_data = [0.266,0.321,0.451,0.704,0.901,1.137]


path_to_data = '/home/luishcc/hdd/free_thread_results/'

def get_snap(dir):
    try:
        with open(dir+'/breaktime.txt', 'r') as fd:
            snap = int(fd.readline())
    except:
        return None
    return snap


R = 6
ratio = 48

A = 50
grid = 1


ini = 6
end = 21

n=0

data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n+1}'
dir = path_to_data + data_case_dir

snap = get_snap(dir)

file = f'correlation_grid1/{snap}.dat'
datafile = '/'.join([dir,file])


data = read_dat(datafile)
x = data['dz']


num = len(x)
if num % 2 == 0:
    row = int((num / 2) + 1)
else:
    row = int((num + 1) / 2)

xx = rfftfreq(num)

sum = np.zeros(row)
sumsq = np.zeros(row)


###############


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
    popt, pcov = opt.curve_fit(gaus, xx2, value[ini:end], p0=[1,mean, sigma], maxfev=2000)

    return xxx[np.argmax(gaus(xxx,*popt))]

#############################################


n = 0
peak = []
peak_array = []
peak_sum = 0
peak_sum2 = 0
while os.path.isfile(datafile):
    print(datafile)
    data = read_dat(datafile)
    arr_real = np.array(data['4'])
    arr = abs(rfft(arr_real))
    p_fit = fit(arr)
    peak.append(p_fit)
    peak_sum += p_fit
    peak_sum2 += p_fit**2
    sum += arr
    sumsq += arr**2
    n += 1
    peak_array.append([peak_sum/n, peak_sum2/n - peak_avg**2)
    data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n+1}'
    dir = path_to_data + data_case_dir
    snap = get_snap(dir)
    file = f'correlation_grid1/{snap}.dat'
    datafile = '/'.join([dir,file])

avg = sum/n
var = sumsq/n - avg**2

peak_avg = peak_sum/n
peak_var = peak_sum2/n - peak_avg**2

from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition,
gaussk
fig, ax = plt.subplots(1,1)

ax.errorbar(np.linspace(1, n, n), peak_array[:][0]*2*np.pi*4.8,
            yerr = np.sqrt(peak_array[:][1])*2*np.pi*4.8, fmt='o',
            ecolor = 'black',markersize=3.5, color='black',
            capsize= 3, capthick=1)

ax.plot([1,n], [func(oh_data[0])]*2)


# ax.set_xlim(0,0.1)
#
# ax.set_title(f'A={-A}')
# ax.set_ylabel(r'$\hat{G}(r,q)$')
# ax.set_xlabel(r'$q$')
# ax.plot(xxx, gaussk)

plt.show()
