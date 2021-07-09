import sys
import os
import numpy as np

import subprocess

sys.path.insert(0, os.path.expanduser('~')+'/md-projects/lampy/io')
import resultsdir as rdir

num_runs = int(sys.argv[1])
num_proc = 8

radius = 6
ratio = 10  # L / 2 Pi R
# linear instability when ratio > 1 (Continuum Theory)
# instability above 0.8 (MDPD Simulation)

length = radius * ratio * 2 * np.pi

seed = np.random.randint(1000, 4000)

A = -50
B = 25
density = 7.0


for i in range(num_runs):
    seed = np.random.randint(1000, 4000)
    save_dir = f'/R[{radius}]ratio[{ratio}]'
    parameters = {'radius':radius,
                  'ratio':ratio,
                  'length':length,
                  'seed':seed,
                  'A':A,
                  'density':density}
    save_dir = rdir.sim_info_files(save_dir, parameters)
    subprocess.run(['mpirun', '-np', f'{num_proc}', 'python3', 'inital.py',
                    f'{radius}', f'{ratio}', f'{seed}', f'{A}', f'{density}',
                    f'{save_dir}'])
