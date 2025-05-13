import numpy as np
import matplotlib.pyplot as plt


file = 'log.lammps'

temp = []
time = []
eng = []
press = []

with open(file, 'r') as fd:
    for line in fd:
        l  = line.split()
        try:
            tt = (float(l[0]))
            tt = (float(l[1]))
            tt = (float(l[5]))
            tt = (float(l[4]))
            # print(line, l[1])
        except Exception as e:
            continue
        time.append(float(l[0]))
        temp.append(float(l[1]))
        press.append(float(l[5]))
        eng.append(float(l[4]))

fig, ax = plt.subplots(3,1)

ax[0].plot(time, temp, 'ko')
ax[0].set_ylim(100,500)

ax[1].plot(time, press, 'ko')
ax[1].set_ylim(-500,500)

ax[2].plot(time, eng, 'ko')
ax[2].set_ylim(-7000,-1000)


plt.show()

