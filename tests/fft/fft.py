import scipy as sp
import numpy as np
from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq
from scipy.fft import dst

from scipy.stats import tmean


import matplotlib.pyplot as plt

num = 500
k = 100
L = np.pi


def func(n, x):
    sum = 0
    for k in range(1,n+1):
        sum += (-1)**(k+1)/k *np.sin(k*x)
    return sum * 2 / np.pi



z = np.linspace(-L, L, num)
r = np.zeros(num)


for i in range(num):
  r[i] = func(k, z[i])

f = (dst(r))
freq = (fftfreq(z.shape[-1]))

plt.figure(1)
plt.plot(z, r)

range = 1
plt.figure(2)
plt.plot(freq[1:len(freq)//range], f.real[1:len(f)//range], 'k.')
# plt.plot(freq, f.real, 'k.')
# plt.plot(freq[:-len(freq)//2], f.imag[:-len(f)//2], 'b-')
plt.show()
