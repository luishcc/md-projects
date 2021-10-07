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


    
plt.figure()
plt.plot(oh, x, label='PRE paper')

# plt.plot([0.3, 0.3], [0.1, 0.7], 'k--')
# plt.plot([1.2, 1.2], [0.1, 0.7], 'k--')

plt.plot([0.311], [0.657], 'ro')

plt.plot([0.359], [0.5416], 'ro')

# plt.plot([0.499], [0.657], 'ro')

#plt.plot([0.762], [0.4166], 'rx')
plt.plot([0.762], [0.4582], 'ro')

#plt.plot([1.214], [0.3749], 'rx')
plt.plot([1.214], [0.5*(0.4166+0.3749)], 'ro')
#plt.plot([1.214], [0.4166], 'rx')


plt.title('Reduced Wavenumber')
plt.ylabel(r'$\chi$')
plt.xlabel(r'$Oh$')
plt.legend(loc=0)
plt.grid(True)
plt.show()
   

