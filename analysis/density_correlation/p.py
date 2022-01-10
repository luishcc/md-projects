import numpy as np
import matplotlib.pyplot as plt


def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)

oh = np.linspace(0.2, 1.50, 10000)
x = np.zeros(len(oh))

for i in range(len(oh)):
    x[i] = func(oh[i])


r50 = 4.85
r60 = 4.75
# r80 = 4.50
r80 = 4.75
# r90 = 4.38
r90 = 5


wl50 = [0.018785, 0.01657]
wl60 = [0.01878, 0.01767]
wl80 = [0.012155, 0.014365]
wl90 = [0.011049]

oh50 = 0.311
oh60 = 0.359
oh80 = 0.762
oh90 = 1.214

plt.figure()
plt.plot(oh, x, label='Theory')

# plt.plot(oh50, 2*np.pi*r50*sum(wl50)/len(wl50), 'ro')
# plt.plot(oh60, 2*np.pi*r60*sum(wl60)/len(wl60), 'ro')
# plt.plot(oh80, 2*np.pi*r80*sum(wl80)/len(wl80), 'ro')
# plt.plot(oh90, 2*np.pi*r90*sum(wl90)/len(wl90), 'ro')

plt.plot(oh50, 2*np.pi*r50*wl50[0], 'ro', label='Simulations')
plt.plot(oh60, 2*np.pi*r60*wl60[0], 'ro')
plt.plot(oh80, 2*np.pi*r80*wl80[1], 'ro')
plt.plot(oh90, 2*np.pi*r90*wl90[0], 'ro')


plt.title('Reduced Wavenumber')
plt.ylabel(r'$\chi$')
plt.xlabel(r'$Oh$')
plt.legend(loc=0)
plt.grid(True)
plt.show()
