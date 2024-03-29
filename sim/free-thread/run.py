import sys
import os
import numpy as np

import subprocess

sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy/io')
import resultsdir as rdir

try:
    num_runs = int(sys.argv[1])
except:
    print("Number of runs not specified, setting num_runs=1")
    num_runs = 1

num_proc = 10

number_dir_from = 20

radius = 4
ratio = 48  # L / 2 Pi R
# linear instability when ratio > 1 (Continuum Theory)
# instability above 0.8 (MDPD Simulation)

num_snapshots = 15000
length = radius * ratio * 2 * np.pi


seed = np.random.randint(1000, 4000)

A = -40
B = 25
density = 6


save_dir = f'R{radius}_ratio{ratio}_A{np.abs(A)}'

if number_dir_from == 1:
    subprocess.run(['mkdir', f'{save_dir}'])    

for i in range(num_runs):
    seed = np.random.randint(1000, 4000)
    parameters = {'radius':radius,
                  'ratio':ratio,
                  'length':length,
                  'seed':seed,
                  'A':A,
                  'density':density}
    save_dir2 = rdir.save_files(save_dir, parameters, number_dir_from)
    subprocess.run(['mpirun', '-np', f'{num_proc}', 'python3', 'initial.py',
                    f'{radius}', f'{ratio}', f'{seed}', f'{A}', f'{density}',
                    f'{save_dir2}', f'{num_snapshots}'])
