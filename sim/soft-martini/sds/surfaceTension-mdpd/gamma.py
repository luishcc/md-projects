import matplotlib.pyplot as plt
import sys

try:
    sc = sys.argv[1]
except IndexError:
    sc = 0.2
    
file = f'sim/{sc}/gamma_{sc}.profile'

time = []
gamma = []

with open(file, 'r') as fd:
    fd.readline()
    fd.readline()    
    while True:
        line = fd.readline()
        try:
            a = line.split()[1]
            b = line.split()[0]            
            gamma.append(float(a))
            time.append(int(b))            
        except:
            break

print(sum(gamma)/len(gamma))

fig, ax = plt.subplots(1,1)
ax.plot(time, gamma)
#plt.show()
