import scipy as sp 
import numpy as np
from scipy.fft import fft, fftfreq, fftshift


import matplotlib.pyplot as plt

def func(k, x):
   return 1 + sp.random.rand()*np.cos(k*x) 
  

num = 1000
k = 0.4
L = 2*np.pi/k


z = np.linspace(0, L, num)
r = np.zeros(num)



for i in range(num):
  r[i] = func(k, z[i])
  
f = fftshift(fft(r))
freq = fftshift(fftfreq(z.shape[-1]))

plt.figure(1)
plt.plot(z, r)

plt.figure(2)
plt.plot(freq, f.real, 'k.')
plt.plot(freq, f.imag, 'b-')
plt.show()
