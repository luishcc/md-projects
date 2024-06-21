import numpy as np 
import matplotlib.pyplot as plt

nt = 3000

Amp = 1
w = 0.01

phi = 0

phi1 = 0
phi2 = np.pi/4
phi3 = np.pi/2

time = np.linspace(0, nt, nt+1)

x1 = Amp*(np.sin(w*time+phi) + w*time*(np.cos(phi1)- np.cos(phi)) - np.sin(phi))
x2 = Amp*(np.sin(w*time+phi) + w*time*(np.cos(phi2)- np.cos(phi)) - np.sin(phi))
x3 = Amp*(np.sin(w*time+phi) + w*time*(np.cos(phi3)- np.cos(phi)) - np.sin(phi))


plt.figure()

plt.plot(time, x1, 'k-', label=r'$\Delta \phi = 0$')
plt.plot(time, x2, 'b--', label=r'$\Delta \phi = \pi/4$')
plt.plot(time, x3, 'g.-', label=r'$\Delta \phi = \pi/2$')
plt.legend(loc='lower left')

plt.ylabel('Position')
plt.xlabel('Time')

plt.show()


