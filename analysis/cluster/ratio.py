import numpy as np
import matplotlib.pyplot as plt



# a = [50,60,70,80,85,90]
a = [0.266, .321, .451, .704, .901, 1.137]

b = [.297, .215, .210, .198, .135, .130]
# b = [.373, .253, .242, .230, .148, .142]


fit = np.polyfit(a,b, 1)
b_fit = [fit[0]*i + fit[1] for i in a ]

a2 = np.linspace(a[0], a[-1], 100)
fit2 = np.polyfit(a, b, 2)
b_fit2 = [fit2[0]*i**2 + fit2[1]*i +fit2[2] for i in a2 ]


plt.figure()

plt.plot(a, b, 'ro', label='Data')
# plt.plot(a, b_fit, 'k--', label='Linear fit')
plt.plot(a2, b_fit2, 'k--', label='Quadratic fit')


plt.title('Ratio of satellite formation')
plt.ylabel('num_satellite / num_total')
plt.xlabel('Oh')
plt.legend(loc=0)
plt.grid(True)
plt.show()
