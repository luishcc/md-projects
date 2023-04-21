import numpy as np

skip = 30

lx = 5
ly = 5
epsilon = np.array([1,2,3])*0.002

def read_file(file, skip=0):
    sum = 0
    n = 0
    with open(file, 'r') as fd:
        for i in range(skip+2):
            fd.readline()
        for line in fd:
            l = line.split()
            sum+=float(l[1])
            n+=1
    return sum/n

fminus = []
fplus = []
for i in range(3):
    file = f'energy-{i+1}.profile'
    fminus.append(read_file(file, skip))
    file = f'energy+{i+1}.profile'
    fplus.append(read_file(file, skip))


file = 'energy.profile'
f = read_file(file, skip)

df_minus = np.array([i-f for i in fminus])
df_plus = np.array([i-f for i in fplus])

da_plus = 2*lx*ly*epsilon
da_minus = -2*lx*ly*epsilon

gamma = 0.5*(df_plus/da_plus + df_minus/da_minus)

# print(fminus, f, fplus)
print(gamma.mean())
print(gamma)

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1)
ax.plot(epsilon, df_plus/da_plus, 'bs')
ax.plot(epsilon, df_minus/da_minus, 'g>')
ax.plot(epsilon, gamma, 'ko')

plt.show()
