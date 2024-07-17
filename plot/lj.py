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

r = np.linspace(3.2,10, 1000)

epsilon = 3

sigma = 4.7
sr = sigma/r
fa1 = 6*(epsilon/sigma)*(2*sr**13-sr**7)

sigma = 4.1
sr = sigma/r
fa2 = 6*(epsilon/sigma)*(2*sr**13-sr**7)

sigma = 3.4
sr = sigma/r
fa3 = 6*(epsilon/sigma)*(2*sr**13-sr**7)

# fa1[r > ] = 0
# fa2[r > .9] = 0
# fa3[r > .8] = 0

fig = plt.figure()
plt.plot(r, fa1, 'r--', markersize=0.4, label=f'4.7')
plt.plot(r, fa2, 'y--', markersize=0.4, label=f'4.1')
plt.plot(r, fa3, 'b--', markersize=0.4, label=f'3.4')


# plt.plot(r, fb1, 'b-.', markersize=0.4, label=f'Repulsive term .75')
# plt.plot(r, fb2, 'g-.', markersize=0.4, label=f'Repulsive term .675')
# plt.plot(r, fb3, 'y-.', markersize=0.4, label=f'Repulsive term .6')

# plt.plot(r, fa1+fb1, 'b-', label=f'Total Force .75')
# plt.plot(r, fa2+fb2, 'g-', label=f'Total Force .675')
# plt.plot(r, fa3+fb3, 'y-', label=f'Total Force .6')


plt.title('Conservative Force')
plt.xlabel(r'$r_{ij}$')
plt.ylabel('F')
plt.legend(loc='upper right')
plt.grid('on')
# plt.yticks([])
# fig.savefig('temp.png', transparent=True)


plt.show()
