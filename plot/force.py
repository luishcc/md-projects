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

r = np.linspace(0,1.2, 1000)

Bb = (15/np.pi)**2*1.65

fa1 = -(1-r)*4.19*15/np.pi/1**4
fa2 = -(1-r/0.9)*4.19*15/np.pi/.9**4
fa3 = -(1-r/0.8)*4.19*15/np.pi/.8**4
fb1 = Bb*(1-r/0.75)**3/.75**7
fb2 = Bb*(1-r/0.675)**3/.675**7
fb3 = Bb*(1-r/0.6)**3/.6**7

fa1[r > 1] = 0
fa2[r > .9] = 0
fa3[r > .8] = 0
fb1[r > .75] = 0
fb2[r > .675] = 0
fb3[r > .6] = 0

fig = plt.figure()
# plt.plot(r, fa1, 'r--', markersize=0.4, label=f'Attractive term')
# plt.plot(r, fa2, 'r--', markersize=0.4, label=f'Attractive term')
# plt.plot(r, fa3, 'r--', markersize=0.4, label=f'Attractive term')


# plt.plot(r, fb1, 'b-.', markersize=0.4, label=f'Repulsive term .75')
# plt.plot(r, fb2, 'g-.', markersize=0.4, label=f'Repulsive term .675')
# plt.plot(r, fb3, 'y-.', markersize=0.4, label=f'Repulsive term .6')

plt.plot(r, fa1+fb1, 'b-', label=f'.75')
plt.plot(r, fa2+fb2, 'g-', label=f'.675')
plt.plot(r, fa3+fb3, 'y-', label=f'.6')


plt.title('Conservative Force')
plt.xlabel(r'$r_{ij}$')
plt.ylabel('F')
plt.legend(loc='upper right')
plt.grid('on')
# plt.yticks([])
# fig.savefig('temp.png', transparent=True)


plt.show()
