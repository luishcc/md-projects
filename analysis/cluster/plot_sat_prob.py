import numpy as np
import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.6*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt


# a = [50,60,70,80,85,90]
a = [0.266, .321, .451, .704, .901, 1.137]

# normal avg
# Main droplet peak
# b = [.297, .215, .210, .198, .135, .130]
# Different peaks
# b = [.373, .253, .242, .230, .148, .142]


# Break_avg
# Different peaks
# b = [.355, .252, .233, .218, .139, .146] # sat/main
b = [.282, .214, .201, .185, .126, .133] # sat/total
# Main droplet peak
# b = [.205, .151, .163, .152, .088, .093] # sat/total


fit = np.polyfit(a,b, 1)
scale = (a[-1] - a[0]) * 0.1
a2 = np.linspace(a[0]-scale, a[-1]+scale, 100)
b_fit = [fit[0]*i + fit[1] for i in a2 ]

a2 = np.linspace(a[0]-scale, a[-1]+scale, 100)
fit2 = np.polyfit(a, b, 2)
b_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in a2 ]


plt.figure()

plt.plot(a, b, 'ko', label='Simulation')
plt.plot(a2, b_fit, 'k--', label='Linear fit')
# plt.plot(a2, b_fit2, 'k--', label='Quadratic fit')



plt.ylabel('$N_{satellite}/N_{total}$')
plt.xlabel('Oh')
plt.legend(loc=0)
# plt.grid(True)
plt.savefig('sat.png', transparent=True)
plt.show()
