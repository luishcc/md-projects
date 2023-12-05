import matplotlib.pyplot as plt 
import numpy as np

dir = '0.5'
dir = '/home/luishcc/hdd/radius_scaling/surfactant/2.3/15'
# dir = '/home/luishcc/hdd/radius_scaling/surfactant/1.6/16'

time = 580
time = 1080
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
print(dz)

with open(f'{dir}/surface_profile/{time}.dat') as fd:
    fd.readline()
    fd.readline()
    for id_z, line in enumerate(fd):
        line = line.split(' ')
        radius = float(line[1])
        # if radius < 0:
        #     radius = abs(radius)
        area = 2*np.pi*radius*dz
        volume = np.pi*radius**2*dz
        print(id_z, radius, dz, area, volume)
        areas.append(area)        
        volumes.append(volume)      
        shape.append(radius)  

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

temp = con[2][:,1] + con[1][:,1]
for type, values in con.items():
    if type == 3: continue
    # ax.plot(values[:,0], values[:,1]/areas, color[type], label=f'{types[type]} Surface')

ax.plot(values[:,0], temp/areas/4, color[type], label=f'Surface')
for type, values in con_bulk.items():
    if type == 3: continue
    ax.plot(values[:,0], values[:,1]/volumes/max(values[:,1]/volumes), color2[type], label=f'{types[type]} Bulk')    

ids = np.linspace(0,1,len(shape))
ax2.plot(ids, volumes/volumes.max(), label='Volume')
ax2.plot(ids, areas/areas.max(), label='Area')
ax2.plot(ids, [i/max(shape) for i in shape], label='shape')
ax.legend()
ax2.legend()

plt.show()



