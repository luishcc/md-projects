import numpy as np
import matplotlib.pyplot as plt

# Set variables
lx = 5
ly = 5
epsilon = np.array([1, 2, 3, 4, 5]) * 0.001

# Define function to read data from energy profile files
def read_file(file):
    eng = []
    with open(file, 'r') as fd:
        for i in range(2):
            fd.readline()
        for line in fd:
            l = line.split()
            eng.append(float(l[1]))
    return np.array(eng)

# Read data from energy profile files
fminus = []
fplus = []
for i in range(3):
    file = f'energy-{i + 1}.profile'
    fminus.append(read_file(file))
    file = f'energy+{i + 1}.profile'
    fplus.append(read_file(file))
file = 'energy.profile'
f = read_file(file)
time = np.linspace(0, 1, len(f))

# Plot energy vs time for the three models and the average energies
fig, ax = plt.subplots(1, 1)
for i in range(3):
    ax.plot(time + i, fplus[i], 'bs', markerfacecolor='none')
    ax.plot(time + i, fminus[i], 'g>', markerfacecolor='none')
    ax.plot([i, i + 1], [fplus[i].mean()] * 2, 'b-')
    ax.plot([i, i + 1], [fminus[i].mean()] * 2, 'g-')
    ax.plot([i, i + 1], [f.mean()] * 2, 'k-')
ax.plot(time, f, 'ko', markerfacecolor='none')
plt.show()
