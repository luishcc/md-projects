import matplotlib.pyplot as plt
from mdpkg.rwfile import read_dat
import os
import numpy as np



dir = 'foo-0'
file = 'ff.dat'
datafile = '/'.join([dir,file])


data = read_dat(datafile)
x = data['x']

sum = np.zeros(len(data['x']))
sumsq = np.zeros(len(data['x']))

n = 0
while os.path.isfile(datafile):
    data = read_dat(datafile)
    arr =np.array(data['1'])
    sum += arr
    sumsq += arr**2
    n += 1
    dir = f'foo-{n}'
    datafile = '/'.join([dir,file])

avg = sum/n
var = sumsq/n - avg**2


plt.figure()
plt.plot(x,avg)
plt.errorbar(x, avg, yerr = np.sqrt(var), fmt='o',ecolor = 'black',color='black')
plt.show()
