# plot all fourier with error bar
import os
import numpy as np

from scipy.fft import rfft, rfftfreq

from mdpkg.rwfile import read_dat, Dat


def sine(x):
    return np.sin(x) + (np.random.random() - 0.5) * 4

x = np.linspace(0,8*np.pi, 80)

num = len(x)
if num % 2 == 0:
    row = int((num / 2) + 1)
else:
    row = int((num + 1) / 2)

for i in range(10):
    dir_out = f'foo-{i}'
    if not os.path.isdir(dir_out):
        os.mkdir(dir_out)
    label='x 1 2 3'
    data = np.zeros((len(x), 4))
    data[:, 0] = x
    dataf = np.empty((row, 4))
    dataf[:, 0] = rfftfreq(len(x))

    for j in range(1,4):
        real = [sine(xx) for xx in x]
        data[:,j] = real
        dataf[:,j] = (rfft(real))


    _dat = Dat(data, labels=label)
    _dat.write_file(f'foo', dir=dir_out)

    _dat = Dat(dataf, labels=label)
    _dat.write_file(f'ff', dir=dir_out)
