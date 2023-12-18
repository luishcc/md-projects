import matplotlib.pyplot as plt 
import numpy as np

def run_snapshot(dir, time):
    # Read surface concentration from .dat file
    with open(f'{dir}/surface_concentration/{time}.dat') as fd:
        line = fd.readline()
        line = line.split(' ')
        num = int(line[4].split('=')[1])
        con_s = np.zeros(num)
        for line in fd:
            line = line.split(' ')
            id = int(line[0])
            value = float(line[1])
            con_s[id] = value
    # Read bulk concentration from .dat file
    with open(f'{dir}/bulk_concentration/{time}.dat') as fd:
        line = fd.readline()
        line = line.split(' ')
        num = int(line[4].split('=')[1])
        con_b = np.zeros(num)
        for line in fd:
            line = line.split(' ')
            id = int(line[0])
            value = float(line[1])
            con_b[id] = value
    # Read surface profile radius from .dat file
    with open(f'{dir}/surface_profile/{time}.dat') as fd:
        line = fd.readline().split(' ')
        dz = float(line[5].split('=')[1])
        num = int(line[6].split('=')[1])
        shape = np.ones(num)*-1
        for id, line in enumerate(fd):
            line = line.split(' ')
            radius = float(line[1])
            shape[id] = radius  
    return shape, con_s, con_b, dz

def get_breaktime(dir):
    with open(f'{dir}/breaktime.txt', 'r') as fd:
        snap = int(fd.readline())-1
    return snap


sc = 2.9
tau = 800
path = f'/home/luishcc/hdd/radius_scaling/surfactant/{sc}'

num_sim = 20
shapes = []
bulk = []
surface = []
for i in range(num_sim):
    dir = f'{path}/{i+1}'
    time = get_breaktime(dir) - tau
    shape, con_s, con_b, dz = run_snapshot(dir, time)
    
    dist = shape.argmin()-int(len(shape)/2)
    shape = np.roll(shape, -dist)
    con_b = np.roll(con_b, -dist)
    con_s = np.roll(con_s, -dist)
    flip = shape.argmin() - shape.argmax() > 0
    if flip: 
        shape = np.flip(shape)
        con_b = np.flip(con_b)
        con_s = np.flip(con_s)
    
    vol = np.pi*shape**2*dz
    area = 2*np.pi*shape*dz

    shapes.append(shape/8.1)
    # bulk.append(con_b/vol*2)
    bulk.append(con_b/area/4)
    surface.append(con_s/area/4)

ids = np.linspace(0.5,len(shapes[0])+0.5, len(shapes[0]))*dz
ids = np.linspace(-.5,.5, len(shapes[0]))


import matplotlib as mpl
dpi = 1600
side = 7
fontsize = 14
rc_fonts = {
    "font.family": "serif",
    "font.size": fontsize,
    'figure.figsize': (0.8*side, .35*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

fig, ax2 = plt.subplots(1,1)

sum = np.zeros(len(shapes[0]))
sumsq = np.zeros(len(shapes[0]))
for con in bulk:
    sum += con
    sumsq += con**2
    # ax.plot(ids, shape, 'c--')
avg = sum/num_sim
var = sumsq/num_sim - avg**2
std = np.sqrt(var)

ax2.plot(ids, avg, 'b--', label=r'Bulk')
ax2.fill_between(ids, avg-std, avg+std, color='lightblue', alpha = 0.6)

sum = np.zeros(len(shapes[0]))
sumsq = np.zeros(len(shapes[0]))
for con in surface:
    sum += con
    sumsq += con**2
    # ax.plot(ids, shape, 'c--')
avg = sum/num_sim
var = sumsq/num_sim - avg**2
std = np.sqrt(var)

ax2.plot(ids, avg, 'k-', label=r'Surface')
ax2.fill_between(ids, avg-std, avg+std, color='gray', alpha = 0.4)



ax2.legend(frameon=False, loc='upper right',  handlelength=1., borderaxespad=0.1, ncol=2,
         columnspacing=0.5,  handletextpad=.2, fontsize=0.9*fontsize)
ax2.plot([-0.6, 0.6], [1.75, 1.75], 'r--')
ax2.text(-0.15, 1.91, r'$\Gamma_{\infty} = 1.75$', fontsize=0.9*fontsize)
ax2.text(-0.45, 2.1, rf'$t_b-t = {tau}$', fontsize=0.9*fontsize)


ax2.set_ylim(-0.01, 2.5)
ax2.set_xlim(-0.51, 0.51)
ax2.set_ylabel(r'$C$ $[N/A_s]$')
ax2.set_xlabel(r'$z/L_z$ $[\cdot]$')


fig.align_ylabels()
fig.tight_layout()

fig.subplots_adjust(hspace=0.15)
# fig.savefig(f'cons-{sc}-{tau}.pdf', dpi=dpi)

plt.show()
    