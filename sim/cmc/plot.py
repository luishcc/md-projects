import os
import numpy as np

import matplotlib as mpl

dpi = 1600
side = 7
rc_fonts = {
    "font.family": "serif",
    "font.size": 12,
    'figure.figsize': (0.8*side, 0.9*side),
    "text.usetex": True
    }
mpl.rcParams.update(rc_fonts)

import matplotlib.pyplot as plt


def run_avg(file):
    gamma = []
    i=0
    flag = True
    sum = 0
    sumsq = 0
    n = 0
    with open(file, 'r') as fd:
        for _ in range(1100):
            fd.readline()
        while flag:
            i+=1
            line = fd.readline()
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
                        sigma = float(line[0])
                        sum += sigma
                        sumsq += sigma**2
                        n += 1
                    except:
                        flag = False
                        break
            if i>=10000:
                break
    avg = sum/n
    std = np.sqrt(sumsq/n - avg**2)
    return  avg, std

surface_t = []
surfactant_c =  []
std_lst = []

for file in os.scandir(os.getcwd()):
    type = file.name.split('.')[-1]
    name = file.name.split('.')[0]
    if type != 'log' or name in ['sc_350']:
    # if type != 'log':
        continue
    print(file.name)
    sc = int(name.split('_')[-1])
    surfactant_c.append(sc)
    st, std = run_avg(file)
    if sc in [100, 150, 200]:
        st *= 40/22
        std *= 40/22
    surface_t.append(st)
    std_lst.append(std)

zip_lst = zip(surfactant_c, surface_t, std_lst)
sort_lst = sorted(zip_lst)
tuples = zip(*sort_lst)
surfactant_c, surface_t, std_lst = [list(tuple) for tuple in tuples]


def to_mol(N):
    NAv = 6.023e23
    V = 8.17**3 * 1e-24
    return N/(V*NAv)

# surfactant_c = [to_mol(i*2) for i in surfactant_c]
surface_t = [(72/7.62)*i for i in surface_t]
std_lst = [(72/7.62)*i for i in std_lst]

# surfactant_c = [i/100 for i in surfactant_c]

fig, ax = plt.subplots(1,1)

# ax.errorbar(surfactant_c, surface_t, yerr = std_lst, fmt='o',
# ecolor = 'black', capsize= 2, capthick=1,color='black', label='Simulation')

ax.plot(surfactant_c, surface_t, 'ko-')
ax.set_xlabel(r'C [$mol/L$]')
ax.set_ylabel(r'$\gamma$ [mN/m]')

plt.tight_layout()
plt.savefig('cmc.pdf', dpi=dpi)

plt.show()
