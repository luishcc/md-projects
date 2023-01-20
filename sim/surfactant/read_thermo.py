import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


# file = 'in_1000.log'
file = 'log.lammps'
file = 'test.log'


energy = []
pressure = []
step = []

i=0
flag = True
with open(file, 'r') as fd:
    for _ in range(157):
        fd.readline()
    while flag:
        print(i)
        i+=1
        line = fd.readline()
        print(line)
        try:
            a = line.split()[0]
        except:
            if i>=1000:
                break
            continue
        if a == 'Step':
            print('TRUE')
            while True:
                try:
                    line = fd.readline().split()
                    step.append(int(line[0]))
                    energy.append(float(line[4]))
                    pressure.append(float(line[5]))
                except:
                    flag = False
                    break
        if i>=1000:
            break

def move_avg(data, num):
    result = []
    for i in range(len(data)-num):
        sum = 0
        for j in range(num):
            sum += data[i+j]
        result.append(sum/num)
    return result

fig, ax = plt.subplots(1,2)

ax[0].plot(step[1:], energy[1:])
ax[0].set_xlabel('Snapshot')
ax[0].set_ylabel('Energy')

ax[1].plot(step[1:], pressure[1:])
ax[1].set_xlabel('Snapshot')
ax[1].set_ylabel('Pressure')

energy2 = savgol_filter(energy[1:], 51, 2)
pressure2 = savgol_filter(pressure[1:], 51, 2)
ax[0].plot(step[1:], energy2, 'k-')
ax[1].plot(step[1:], pressure2, 'k-')

num = 1000
ene_avg = move_avg(energy[1:], num)
pre_avg = move_avg(pressure[1:], num)

ax[0].plot(step[1:-num], ene_avg, 'g-')
ax[1].plot(step[1:-num], pre_avg, 'g-')
ax[0].grid(True)
ax[1].grid(True)
plt.show()
