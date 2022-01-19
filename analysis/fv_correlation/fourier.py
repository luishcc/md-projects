import sys
import os

import numpy as np
from scipy.fft import rfft, rfftfreq
# from scipy.fft import fft, fftfreq

from mdpkg.rwfile import read_dat, Dat



# dir = 'thread/force_r'
# dir = 'thread/cross'
dir = 'thread/velocity_z'
# dir = 'thread/density'
dir_out = '/'.join([dir, 'fourier'])

if not os.path.isdir(dir_out):
    os.mkdir(dir_out)

with open(dir+'/0.dat') as f:
    labels = f.readline()
    labels = labels.split()[1:]
    labels[0] = 'freq'
    labels = ' '.join(labels)


snap = 0
file = dir + f'/{snap}.dat'
while os.path.isfile(file):
    print(file)
    data = read_dat(file)

    num = len(data['dz'])-1
    if num % 2 == 0:
        row = int((num / 2) + 1)
    else:
        row = int((num + 1) / 2)

    col = len(data)
    fourier = np.empty((row, col))
    fourier[:,:] = np.NaN
    for i in range(1, col):
        if not np.any(np.isnan(data[str(i-1)])):
            # fourier[:, i] = abs(rfft(data[str(i-1)]))
            fourier[:, i] = rfft(data[str(i-1)][1:])
    fourier[:,0] = rfftfreq(num)

    fourier_dat = Dat(fourier, labels=labels)
    fourier_dat.write_file(f'{snap}', dir=dir_out)
    snap += 6
    file = dir + f'/{snap}.dat'
