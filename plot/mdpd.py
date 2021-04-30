import numpy as np
import matplotlib.pyplot as plt


def total_force(x, a, b):
    a = attractive(a) * weight(x, cutoff=1)
    b = repulsive(x, b) * weight(x, cutoff=0.75)
    return a + b

def weight(x, cutoff=1):
    if x <= cutoff:
            w = 1 - x/cutoff
    else:
        w = 0
    return w

def attractive(a):
    return a

def local_density(x, cutoff=0.75):
    rho = (15/(2*np.pi*cutoff)) * (weight(x,cutoff))**2
    return rho

def repulsive(x, b):
    return b * 2 * local_density(x)


r = np.linspace(0,1.5,1000)
f_a = np.zeros(len(r))
f_b = np.zeros(len(r))
f = np.zeros(len(r))

A = -50
B = 25

for i in range(len(r)):
    f_a[i] = -1*attractive(A) * weight(r[i])
    f_b[i] = -1*repulsive(r[i], B) * weight(r[i], cutoff=0.75)
    f[i] = f_a[i]+f_b[i]

plt.figure()
plt.plot(r, f_a, 'r--', markersize=0.4, label=f'Attractive term A={A}')
plt.plot(r, f_b, 'b--', markersize=0.4, label=f'Repulsive term B={B}')
plt.plot(r, f, 'k-', label=f'Total Force')
plt.title('Conservative Force')
plt.xlabel('r_ij')
plt.ylabel('F')
plt.legend(loc='lower right')
plt.grid('on')
plt.show()
