import numpy as np 
import matplotlib.pyplot as plt

def lj(x, sigma=4.7, epsilon=3.5):
    frac = sigma/x
    return 24*(epsilon/sigma) * (2*frac**13 - frac**7)

def mdpd(x, a=-26, b=7.91, rc=1, rd=0.75  ):
    wc = 1-x/rc
    wd = 1-x/rd
    rho = 15/(2*np.pi*rd**3)*wd**2
    att = a/rc**4*wc
    att[ x > rc] = 0
    rep = b/rd**4*wd*2*rho
    rep[ x > rd] = 0
    return att+rep

rij = np.linspace(0.25, 1.3, 10000)

fig, (ax1, ax2) = plt.subplots(1,2)

ax1.plot([rij[0], rij[-1]], [0,0], 'k--')
ax1.plot(rij, mdpd(rij), label = 'C1')
ax1.plot(rij, mdpd(rij, rd=0.65, rc=.65/.65, a=-26*.75), label = 'sC1')
ax1.set_ylim(-15,10)
ax1.legend(frameon=False)

rij *= 8.54
ax2.plot([rij[0], rij[-1]], [0,0], 'k--')
ax2.plot(rij, lj(rij), label = 'C1')
ax2.plot(rij, lj(rij, sigma=4.3, epsilon=.75*3.5), label = 'sC1')
ax2.set_ylim(-2,2)
ax2.legend(frameon=False)

plt.show()