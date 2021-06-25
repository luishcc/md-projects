import numpy as np
import scipy as sp
import os



import matplotlib.pyplot as plt

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi

def readVor(file_name):
    pos = []
    surf = []
    vol = []
    file = open(file_name, 'r')
    reading_entry = False

    for line in file:

        if line.find('ITEM: ATOMS') >= 0:
            reading_entry = True
            continue

        if reading_entry:
            l = line.split()
            coo = [float(l[2]), float(l[3]), float(l[4])]
            pos.append(coo)
            vol.append(float(l[5]))
            if float(l[5]) > .3:
                surf.append(coo)
    return pos, surf, vol


pos, surf, volumes = readVor('dump.voro')



px = [sub[0] for sub in pos]
py = [sub[1] for sub in pos]
pz = [sub[2] for sub in pos]

sx = [sub[0] for sub in surf]
sy = [sub[1] for sub in surf]
sz = [sub[2] for sub in surf]

radius = 6

sr = np.zeros(len(sx))
st = np.zeros(len(sx))
sig = []
sig2 = []
z = []
for i in range(len(sx)):
    sr[i], st[i] = cart2pol(sx[i], sy[i])
    if -0.4 < st[i]*radius < 0.4:
        sig.append(sr[i]-radius)
        sig2.append(sr[i])
        z.append(sz[i])



from scipy.fft import fft, fftfreq, fftshift, rfft, rfftfreq

# f = fftshift(fft(sig))
# freq = fftshift(fftfreq(len(z)))

f = rfft(sig) / len(sig)
freq = rfftfreq(len(z))


plt.figure(1)
plt.subplot(121)
plt.plot(z, sig2, 'k.')
plt.plot([0,60], [6, 6], 'k--')
plt.ylim(0,9)


plt.subplot(122)
plt.plot(freq, f.real, 'k-')
# plt.plot(freq, f.imag, 'b-')

# spec = np.abs(f)**2

# plt.subplot(133)
# plt.plot(freq, spec/max(spec), 'b-')

plt.show()
