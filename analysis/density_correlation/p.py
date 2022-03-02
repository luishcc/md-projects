import numpy as np
import matplotlib.pyplot as plt


def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)

oh = np.linspace(0.2, 1.30, 10000)
x = np.zeros(len(oh))

for i in range(len(oh)):
    x[i] = func(oh[i])


r=5.75
# r=6

r50 = r
r60 = r
r70 = r
r80 = r
r85 = r
r90 = r

wl50 = [0.01626563]
wl60 = [0.01482813]
wl70 = [0.013125, 0.01409375]
wl80 = [0.01246875]
wl85 = [0.0105625]
wl90 = [0.010625]

# oh50 = 0.315

oh50 = 0.266
oh60 = 0.321
oh70 = 0.451
oh80 = 0.704
oh85 = 0.901
oh90 = 1.137

plt.figure()
plt.plot(oh, x, label='Theory')


plt.plot(oh50, 2*np.pi*r50*wl50[0], 'ro', label='Simulations')
plt.plot(oh60, 2*np.pi*r60*wl60[0], 'ro')
# plt.plot(oh70, 2*np.pi*r70*wl70[0], 'ro')
plt.plot(oh70, 2*np.pi*r70*wl70[1], 'ro')
plt.plot(oh80, 2*np.pi*r80*wl80[0], 'ro')
plt.plot(oh85, 2*np.pi*r85*wl85[0], 'ro')
plt.plot(oh90, 2*np.pi*r90*wl90[0], 'ro')


plt.title('Reduced Wavenumber')
plt.ylabel(r'$\chi$')
plt.xlabel(r'$Oh$')
plt.legend(loc=0)
plt.grid(True)
plt.show()
