import numpy as np
import matplotlib.pyplot as plt


def func(x):
    b = x*np.sqrt(18)
    a = 1/(2+b)
    return np.sqrt(a)

oh = np.linspace(0.2, 1.30, 10000)
x = np.zeros(len(oh))

x = func(oh)

# for i in range(len(oh)):
#     x[i] = func(oh[i])


# r=5.7
r=4.7
#r=6


R = 6
ratio = 48

A = [50, 60, 70, 80, 85, 90]
oh_data = [0.266,0.321,0.451,0.704,0.901,1.137]

q = []
q_var = []
for iter, a in enumarate(A[:4]):
    file = f'R{R}_ratio{ratio}_A{a}-peak.csv'
    with open(file, 'r') as fd:
        line = fd.readline().split(',')
        q.append(line[0])
        q_var.append(line[1])



plt.figure()
plt.plot(oh, x, label='Theory')

plt.errorbar(oh_data[:4], q, yerr = np.sqrt(q_var), fmt='o',ecolor = 'black',color='black')

plt.title('Reduced Wavenumber')
plt.ylabel(r'$\chi$')
plt.xlabel(r'$Oh$')
plt.legend(loc=0)
plt.grid(True)
plt.show()
