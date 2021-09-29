from ovito.io import *
from ovito.modifiers import *

from scipy.linalg import eig, inv
import numpy as np

from mdpkg.rwfile import Dat


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

dir = '/home/luishcc/hdd/free_thread_results/R6_ratio6_A50-4/'
file = 'thread.lammpstrj'

pipeline = import_file(dir+file)

clt_mod = ClusterAnalysisModifier(cutoff = 0.8,
                                  compute_gyration = True,
                                  sort_by_size = True)

pipeline.modifiers.append(clt_mod)

labels = 'id size radius asphericity acylindricity anisotropy'

for i in range(50, 200):

    data = pipeline.compute(i)
    cluster_table = data.tables['clusters']
    print(i)

    a = cluster_table['Radius of Gyration'][...]
    b = cluster_table['Cluster Size'][...]
    c = cluster_table['Gyration Tensor'][...]

    ncl = len(a)
    dat = np.zeros((ncl, 6))

    for j in range(ncl):
        dat[j, 0] = j
        dat[j, 1] = b[j]
        dat[j, 2] = a[j]
        ev = get_eig(c[j])
        dat[j, 3] = asphericity(ev)
        dat[j, 4] = acylindricity(ev)
        dat[j, 5] = anisotropy(ev)

    save = Dat(dat, labels)
    save.write_file(f'{i}')

    print(a, '\n', b, '\n', c)
    print()

# export_file(pipeline, f'{i}.dat', 'txt/table', key='clusters')
