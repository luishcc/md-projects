import matplotlib.pyplot as plt 
import numpy as np

dir = '0.5'
# dir = '2.9'

# dir = '/home/luishcc/hdd/radius_scaling/surfactant/2.3/15'
# dir = '/home/luishcc/hdd/radius_scaling/surfactant/1.6/16'

time = 320
# time = 1320

con = {}
with open(f'{dir}/surface_concentration/{time}.dat') as fd:
    fd.readline()
    for line in fd:
        line = line.split(' ')
        id = int(line[0])
        value = float(line[1])
        con[id] = value

con_bulk = {}
with open(f'{dir}/bulk_concentration/{time}.dat') as fd:
    fd.readline()
    for line in fd:
        line = line.split(' ')
        id = int(line[0])
        value = float(line[1])
        con_bulk[id] = value

areas = []
volumes = []
shape = []
with open(f'{dir}/surface_profile/{time}.dat') as fd:
    line = fd.readline().split(' ')
    dz = float(line[5].split('=')[1])
    for id_z, line in enumerate(fd):
        line = line.split(' ')
        radius = float(line[1])
        area = 2*np.pi*radius*dz
        volume = np.pi*radius**2*dz
        print(id_z, radius, dz, area, volume)
        areas.append(area)        
        volumes.append(volume)      
        shape.append(radius)  

con = np.array([value for _, value in sorted(con.items())])
con_bulk = np.array([value for _, value in sorted(con_bulk.items())])
areas = np.array(areas)
volumes = np.array(volumes)

fig, (ax,ax2) = plt.subplots(2,1)

ids = np.linspace(0,1,len(shape))

ax.plot(ids, con/areas/4, 'k-', label='Surface')
ax.plot(ids, con_bulk/volumes, 'b-', label='Bulk')    
ax.legend()

ax2.plot(ids, volumes/volumes.max(), label='Volume')
ax2.plot(ids, areas/areas.max(), label='Area')
ax2.plot(ids, [i/max(shape) for i in shape], label='shape')
ax2.legend()

plt.show()



