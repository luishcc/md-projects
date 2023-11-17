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

con_bulk = {}
with open(f'{dir}/bulk_concentration/{time}.dat') as fd:
    fd.readline()
    for line in fd:
        line = line.split(' ')
        type = int(line[1])
        id_z = int(line[0])
        value = float(line[2])
        con_bulk.setdefault(type, []).append([id_z, value])        

areas = []
volumes = []
shape = []
with open(f'{dir}/surface_profile/{time}.dat') as fd:
    fd.readline()
    fd.readline()
    line = fd.readline().split(' ')
    dz = -float(line[0])
    line = fd.readline().split(' ')
    dz += float(line[0])
with open(f'{dir}/surface_profile/{time}.dat') as fd:
    fd.readline()
    fd.readline()
    for id_z, line in enumerate(fd):
        line = line.split(' ')
        radius = float(line[1])-1
        area = 2*np.pi*radius*dz
        volume = np.pi*radius**2*dz
        print(radius, dz, area, volume)
        areas.append(area)        
        volumes.append(volume)      
        shape.append(radius)  

print(dz)

# Dict where each atom type is a key and 
# value is a list of lists [[binID, numAtoms], ...]        
con = {key: np.array(lst) for key, lst in con.items()}
con_bulk = {key: np.array(lst) for key, lst in con_bulk.items()}
areas = np.array(areas)
volumes = np.array(volumes)


fig, (ax,ax2) = plt.subplots(2,1)

types =  {1:'H', 2:'T', 3:'W'}
color = {1:'r--', 2:'g--', 3:'b--'}
color2 = {1:'r-', 2:'g-', 3:'b-'}

for type, values in con.items():
    ax.plot(values[:,0], values[:,1]/areas, color[type], label=types[type])
for type, values in con_bulk.items():
    ax.plot(values[:,0], values[:,1]/volumes, color2[type], label=types[type])    

ids = np.linspace(0,1,len(shape))
ax2.plot(ids, volumes/volumes.max(), label='Volume')
ax2.plot(ids, areas/areas.max(), label='Area')
ax2.plot(ids, [i/max(shape) for i in shape], label='shape')
ax.legend()
ax2.legend()

plt.show()



