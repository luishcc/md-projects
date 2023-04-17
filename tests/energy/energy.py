import numpy as np

file = 'energy.lammpstrj'

rc = 1
rd = 0.75
A = -50
B = 25

density_cc = 15/(2*np.pi*rc**3)
density_cd = 15/(2*np.pi*rd**3)
energy_cc = np.pi*rc**4*A/30
energy_cd = np.pi*rd**4*B/30

def read_snap(file):
    atoms = {}
    file.readline()
    timestep = int(file.readline())
    file.readline()
    num = int(file.readline())
    for i in range(5):
        file.readline()
    for i in range(num):
        line = file.readline().split()
        id = int(line[0])
        x = float(line[1])
        y = float(line[2])
        z = float(line[3])
        atoms[id] = [x, y, z]
    return atoms

def distance(a1, a2):
    xxsq = (a1[0] - a2[0])**2
    yysq = (a1[1] - a2[1])**2
    zzsq = (a1[2] - a2[2])**2
    return np.sqrt(xxsq+yysq+zzsq)

with open(file, 'r') as fd:
    atoms = read_snap(fd)
    local_densities_c = {}
    local_densities_d = {}
    self_energy_a = {}
    self_energy_b = {}
    U = {}

    for i, a1 in atoms.items():
        dc = 0
        dd = 0
        for j, a2 in atoms.items():
            wd = 0
            wc = 0
            if i == j:
                continue
            rij = distance(a1,a2)
            if rij < rd:
                wd = (1-rij/rd)
                dd += density_cd*wd**2
            if rij < rc:
                wc = (1-rij/rc)
                dc += density_cc*wc**2
                print(i, j, wc, wd)

        local_densities_c[i] = dc
        local_densities_d[i] = dd
        self_energy_a[i] = energy_cc*dc
        self_energy_b[i] = energy_cd*dd**2
        U[i] = (self_energy_a[i]+self_energy_b[i])

        # print(i,  wcsumsq, (1/rd)**2, wdsumsq)
