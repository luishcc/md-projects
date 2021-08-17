from readLammps import DumpReader
import numpy as np


file = 'box.dump'

trj = DumpReader(file)


def distance(p1, p2):
    sum = 0
    for a,b in zip(p1,p2):
        sum += (a-b)**2
    return np.sqrt(sum)

n_atoms = len(trj.atoms)

dist = 0
pair = 0
for i in range(n_atoms):
    print(i, ' / ', n_atoms)
    p1 = trj.atoms[i].x
    for j in range(i+1,n_atoms):
        p2 = trj.atoms[j].x
        dist += distance(p1 , p2)
        pair += 1

print(dist/pair)
