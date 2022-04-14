import numpy as np
import matplotlib.pyplot as plt



a = [50,60,70,80,85,90]
b = [.297, .215, .210, .198, .135, .130]
# b = [.373, .253, .242, .230, .148, .142]


plt.figure()
# plt.plot(oh, x, label='Theory')


plt.plot(a, b, 'ro--')


plt.title('Ratio of satellite formation')
plt.ylabel('num_satellite / num_total')
plt.xlabel('-A')
# plt.legend(loc=0)
plt.grid(True)
plt.show()
