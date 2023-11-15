import matplotlib.pyplot as plt 
import numpy as np

dir = '0.5'

time = 240
con = {}
with open(f'{dir}/surface_concentration/{time}.dat') as fd:
    fd.readline()
    for line in fd:
        line = line.split(' ')
        type = int(line[1])
        id_z = int(line[0])
        value = float(line[2])
        con.setdefault(type, []).append([id_z, value])
        
con = {key: np.array(lst) for key, lst in con.items()}

fig, ax = plt.subplots(1,1)

types =  {1:'H', 2:'T', 3:'W'}
color = {1:'r-', 2:'g-', 3:'b-'}

for type, values in con.items():
    ax.plot(values[:,0], values[:,1], color[type], label=types[type])
ax.legend()

plt.show()



