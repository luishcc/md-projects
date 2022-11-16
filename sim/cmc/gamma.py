import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


file = 'sc_200.log'

gamma = []

i=0
flag = True
with open(file, 'r') as fd:
    for _ in range(1100):
        fd.readline()
    while flag:
        print(i)
        i+=1
        line = fd.readline()
        print(line)
        try:
            a = line.split()[0]
        except:
            if i>=100000:
                break
            continue
        if a == 'v_gamma':
            print('TRUE')
            for i in range(30):
                fd.readline()
            while True:
                try:
                    line = fd.readline().split()
                    gamma.append(float(line[0]))
                except:
                    flag = False
                    break
        if i>=10000:
            break

print(sum(gamma)/len(gamma))

fig, ax = plt.subplots(1,1)
ax.plot(np.linspace(0,1, len(gamma)), gamma)
plt.show()
