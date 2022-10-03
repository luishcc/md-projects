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

# Main droplet break_avg
b = [9.545, 9.589, 9.923, 10.649, 10.969, 11.335]
c = [1.248, 1.151, 1.234, 1.109, 1.222, .932]

# Main droplet break_avg_peak
# b2 = [10.064, 10.136, 10.647, 11.33, 11.606, 11.765]
# c2 = [1.42, 1.42, 1.4, 1.24, 1.14, 1.02]
#
# # Main droplet normal_avg
# b3 = [9.547, 9.541, 10.042, 10.722, 10.819, 11.4]
# c3 = [1.278, 1.111, 1.234, 1.12, 1.322, .876]


wave = [.018927425365090515, .017959188701441885, .016553644129911244,
.014737153310297676, .013920311412504544, .01340404171055144]
# wave = [1/i for i in wave]
wave = [i*2*np.pi*4.8 for i in wave]

q_var = [3.156327982930347e-06,
2.328394395880221e-06,
1.8893985765694086e-06,
2.054396275751638e-06,
3.954677744054939e-06,
9.193559899539904e-06]
# q_var = [i*2*np.pi*4.8 for i in q_var]



#
# fit = np.polyfit(a,b, 1)
# b_fit = [fit[0]*i + fit[1] for i in a ]
#
# a2 = np.linspace(a[0], a[-1], 100)
# fit2 = np.polyfit(a, b, 2)
# b_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in a2 ]


def pred(x):
    scale = 0.8
    return np.cbrt(0.75*(6*scale)**2*x-1.2**3)
    # return np.cbrt(0.75*(6*1)**2*x-8.6**3)


def pred2(x):
    scale = 1.012
    return 0.75*(6*scale)**2*x-8.7**3


def pred3(x):
    scale = 0.8
    return np.cbrt(0.75*(6*scale)**2/x)

def pred4(x):
    scale = 0.8
    return (6*scale)*np.cbrt(1.5*np.pi/x)

plt.figure()

# plt.plot(wave, b, 'ko', label='Simulation')

plt.errorbar(wave, b, xerr = np.sqrt(q_var)*2*np.pi*4.8,
fmt='o',ecolor = 'black',color='black', label='Simulation')

dv = abs(wave[-1]-wave[0])
pdv = 0.3 * dv
x = np.linspace(wave[0]+pdv, wave[-1]-pdv, 100)
plt.plot(x, pred4(x), 'k--', label='Theory')

# plt.xlabel('$\lambda$ $[r_c]$')
plt.xlabel('$\chi$')
plt.ylabel('$R_D$ $[r_c]$')
plt.legend()
plt.savefig('rel.png', transparent=False)

plt.show()
