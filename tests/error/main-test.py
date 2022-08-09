from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
from mdpkg.rwfile import read_dat
import os
import numpy as np


path_to_data = '/home/luishcc/hdd/free_thread_results/'


R = 6
ratio = 48
A = 50
grid = 1

snap = 170

n=0

data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n+1}'
dir = path_to_data + data_case_dir

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

n = 0
while os.path.isfile(datafile):
    data = read_dat(datafile)
    arr_real = np.array(data['6'])
    arr = abs(rfft(arr_real))
    sum += arr
    sumsq += arr**2
    n += 1
    data_case_dir = f'R{R}_ratio{ratio}_A{A}-{n+1}'
    dir = path_to_data + data_case_dir
    datafile = '/'.join([dir,file])

avg = sum/n
var = sumsq/n - avg**2


plt.figure()
plt.plot(xx,avg)
plt.errorbar(xx, avg, yerr = np.sqrt(var), fmt='o',ecolor = 'black',color='black')
plt.show()
