import numpy as np
import matplotlib.pyplot as plt


def viscous(t, Oh):
  return (0.0709/Oh) * t 
  
def inertial(t, Oh):
  return (0.0709/Oh) * t**(2/3)

def viscoinertial(t, Oh):
  return (0.0304/Oh) * t

def thermal(t, h0):
  return h0 * t**0.418

def exponential(t,a):
  return np.exp(a*t)

Oh = [100]

t = np.linspace(-100,400, 1000)
t2 = np.linspace(0,100, 1000)

fig, ax = plt.subplots(1,1)
for o in Oh:
  # ax.plot(t, inertial(t,o), label=f'I {o}')
  ax.loglog(t, 100*viscous(t,o), label=f'V {o}')
  # ax.plot(t, viscoinertial(t,o), label=f'VI {o}')

ax.plot(t2, 100*thermal(t2,0.05), label=f'TF')
ax.plot(t2, exponential(t2,0.05), label=f'Exp')
# ax.set_ylim(0,0.6)
ax.legend()
plt.show()
