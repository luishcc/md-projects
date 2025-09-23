import os
os.environ['OVITO_GUI_MODE'] = '1'
from ovito.io import *
from ovito.modifiers import *

from scipy.linalg import eig, inv
import numpy as np

path_to_mdpd = 'phase-mdpd/25/sds.lammpstrj'
path_to_md = 'phase-martini/25/sds.lammpstrj'


def asphericity(lst):
    return abs(lst[2] - 0.5 * (lst[0]+lst[1]))

def anisotropy(lst):
    n = (lst[0]**2+lst[1]**2+lst[2]**2)
    d = (lst[0]+lst[1]+lst[2])**2
    return abs(1.5 * n / d - 0.5)

def acylindricity(lst):
    return abs(lst[1] - lst[0])

def get_eig(d):
    gy = np.array([[d[0], d[3], d[4]],
                   [d[3], d[1], d[5]],
                   [d[4], d[5], d[2]]])
    eva, eve = eig(gy)
    eva.sort()
    return eva

labels = ['size', 'radius', 'asphericity', 'acylindricity', 'anisotropy']


def run_cluster(path, cutoff, snap=1000000):
    
    pipeline = import_file(path)
    
    slt_mod = SelectTypeModifier(types=[2])
    pipeline.modifiers.append(slt_mod)
    clt_mod = ClusterAnalysisModifier(
        cutoff=cutoff, 
        compute_gyration=False,
        only_selected=True)
    pipeline.modifiers.append(clt_mod)
    data = pipeline.compute(snap)
    
    cluster_table = data.tables['clusters']
    # a = cluster_table['Radius of Gyration'][...]
    b = cluster_table['Cluster Size'][...]
    # c = cluster_table['Gyration Tensor'][...]

    ncl = len(b)
    table = np.zeros((ncl, 5))

    for j in range(ncl):
        table[j, 0] = b[j]/3
        # table[j, 1] = a[j]
        # ev = get_eig(c[j])
        # table[j, 2] = asphericity(ev)
        # table[j, 3] = acylindricity(ev)
        # table[j, 4] = anisotropy(ev)
    
    return table

md = []
mdpd = []
for i in range(1):
    print('md ',i)
    dt = run_cluster(path_to_md, 8, snap=10000)
    for size in dt[:,0]:
        md.append(size)

for i in range(1):
    print('mdpd ',i)
    dt = run_cluster(path_to_mdpd, 0.7, snap=10000)
    for size in dt[:,0]:
        mdpd.append(size)

import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1)

ax.hist(md, label='md', alpha=0.4, density=True, bins=20)
ax.hist(mdpd, label='mdpd', alpha=0.4, density=True, bins=20)
ax.legend()

md = np.array(md)
mdpd = np.array(mdpd)

print('md ', md.mean(), md.std())
print('mdpd ', mdpd.mean(), mdpd.std())

plt.show()

##################################################
##################################################
# OLD BELOW

# from mdpkg.rwfile import Dat, CSV

# import os
# import sys

# save = CSV(table, labels)
# save.write_file(f'{i}', dir=save_dir)

# print(a, '\n', b, '\n', c)
# print()



# for i in range(initial_step, pipeline.source.num_frames):
#     if i >= final_step:
#         break
#     data = pipeline.compute(i)
#     cluster_table = data.tables['clusters']
#     print(i)

#     a = cluster_table['Radius of Gyration'][...]
#     b = cluster_table['Cluster Size'][...]
#     c = cluster_table['Gyration Tensor'][...]

#     ncl = len(a)
#     table = np.zeros((ncl, 5))

#     for j in range(ncl):
#         table[j, 0] = b[j]
#         table[j, 1] = a[j]
#         ev = get_eig(c[j])
#         table[j, 2] = asphericity(ev)
#         table[j, 3] = acylindricity(ev)
#         table[j, 4] = anisotropy(ev)

#     save = CSV(table, labels)
#     save.write_file(f'{i}', dir=save_dir)

#     # print(a, '\n', b, '\n', c)
#     # print()

#     n += 1
#     # data_case_dir = f'R{R}_ratio{ratio}_A{abs(A)}/{n}'
#     # dir = path_to_data + data_case_dir

#     case += 1
#     dir = path_to_data + '/' + str(case)

#     save_dir = dir + f'/cluster'


# export_file(pipeline, f'{i}.dat', 'txt/table', key='clusters')
# pandas.read_csv('dat', sep=' ', header=0, names=[labels])
