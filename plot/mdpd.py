import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.9*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)


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
    rho = (15/(2*np.pi*cutoff**3)) * (weight(x,cutoff))**2
    return rho

def repulsive(x, b):
    return b * 2 * local_density(x)


r = np.linspace(0,1.5,1000)
f_a = np.zeros(len(r))
f_b = np.zeros(len(r))
f_b2 = np.zeros(len(r))
f = np.zeros(len(r))
f2 = np.zeros(len(r))
w_p = np.zeros(len(r))

A = -50
B = 25
pp = 3


for i in range(len(r)):
    f_a[i] = 1*attractive(A) * weight(r[i])
    f_b[i] = 1*repulsive(r[i], B) * weight(r[i], cutoff=0.75)
    f_b2[i] = 1*2*B*pp * weight(r[i], cutoff=0.75)
    f[i] = f_a[i]+f_b[i]
    f2[i] = f_a[i]+f_b2[i]
    w_p[i] = local_density(r[i])

fig = plt.figure()
plt.plot(r, f_a, 'r--', markersize=0.4, label=f'Attractive term')
# plt.plot(r, f_b, 'b--', markersize=0.4, label=f'Repulsive term')
# plt.plot(r, f, 'k-', label=f'Total Force')

plt.plot(r, [0]*len(r), 'k--')

plt.plot(r, f_b2, 'b--', markersize=0.4, label=f'Repulsive term')
plt.plot(r, f2, 'k-', label=f'Total Force')


plt.title('Conservative Force')
plt.xlabel(r'$r_{ij}$')
plt.ylabel('F')
plt.legend(loc='upper right')
# plt.grid('on')
plt.yticks([])
fig.savefig('temp.png', transparent=True)


# plt.figure(2)
# plt.plot(r, w_p, 'r--', markersize=0.4)
# plt.title('Local Density Weight Function')
# plt.xlabel('r_ij')
# plt.ylabel('W_\rho')
# plt.grid('on')

plt.show()
