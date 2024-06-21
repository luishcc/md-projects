import numpy as np 
import matplotlib.pyplot as plt

nt = 10000
dt = 0.01

v0 = 1
f0 = 1
x0 = 0

w = 1

def g(time):
    return np.sin(w*time + np.pi/6) +0.5*time

# def g(time):
#     return 0.1*time

x1 = x0 + dt*v0

x = [x0, x1]

# x'' + wx = g(t)

for t in range(2,nt):
    xn = (g((t-1)*dt) - w**2*x[t-1])*dt**2 + 2*x[t-1] - x[t-2]
    x.append(xn)

plt.figure()
plt.plot(np.linspace(0,nt,nt), x, 'k.')
plt.show()


