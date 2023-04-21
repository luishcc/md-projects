import numpy as np

lx = 5
ly = 5
epsilon = np.array([1,2,3,4,5])*0.001

def read_file(file):
    eng = []
    with open(file, 'r') as fd:
        for i in range(2):
            fd.readline()
        for line in fd:
            l = line.split()
            eng.append(float(l[1]))
    return eng

file = f'energy-{3}.profile'
temp = np.array(read_file(file))
f = [temp.mean()]
file = f'energy-{2}.profile'
temp = np.array(read_file(file))
f += [temp.mean()]
file = f'energy-{1}.profile'
temp = np.array(read_file(file))
f += [temp.mean()]
file = f'energy.profile'
temp = np.array(read_file(file))
f += [temp.mean()]
file = f'energy+{1}.profile'
temp = np.array(read_file(file))
f += [temp.mean()]
file = f'energy+{2}.profile'
temp = np.array(read_file(file))
f += [temp.mean()]
file = f'energy+{3}.profile'
temp = np.array(read_file(file))
f += [temp.mean()]

time = np.linspace(0,1, len(f))

import matplotlib.pyplot as plt

window = 1
average_f = []
for ind in range(len(f) - window + 1):
    average_f.append(np.mean(f[ind:ind+window]))
for ind in range(window - 1):
    average_f.insert(0, np.nan)



n = 0
fig, ax = plt.subplots(1,1)
# for i in range(3):
    # ax.plot(time+i, fplus[i], 'bs', markerfacecolor='none')
    # ax.plot(time+i, fminus[i], 'g>', markerfacecolor='none')
    # ax.plot([i,i+1], [fplus[i].mean()]*2, 'b-')
    # ax.plot([i,i+1], [fminus[i].mean()]*2, 'g-')

    # ax.plot([i,i+1], [f.mean()]*2, 'k-')
# ax.plot(time, f, 'ko', markerfacecolor='none')

# ax.plot(time, average_f, 'ko', markerfacecolor='none')
ax.plot(time, f, 'ko', markerfacecolor='none')

plt.show()
