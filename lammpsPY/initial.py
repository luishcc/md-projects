from mpi4py import MPI
from lammps import lammps
import numpy as np
import os
import sys
import gen

radius = 6.0
wave_number = 0.6
wave_length = 2 * np.pi * radius / wave_number

lmp = lammps()

initial_commands = [
    "units lj",
    "dimension 3",
    "boundary p p p",
    "neighbor 0.3 bin",
    "neigh_modify every 1 check yes",
    "atom_style  mdpd"
]

create_commands = [
    f"region  mdpd  block -18 18 -18 18 0 {wave_length} units box",
    "create_box 1 mdpd",
    "lattice  fcc 6.05",
    f"region tube cylinder z 0 0 {radius} INF INF",
    "create_atoms  1 region tube",
    "mass 1 1.0"
]

pair_commands = [
    "pair_style hybrid/overlay mdpd/rhosum mdpd 1.0 1.0 9872598",
    "pair_coeff 1 1 mdpd/rhosum  0.75",
    "pair_coeff 1 1 mdpd -40 25 18.0 1.0 0.75"
]

sim_commands = [
    "compute             mythermo all temp",
    "thermo              100",
    "thermo_modify       temp mythermo",
    "thermo_modify       flush yes",
    "velocity            all create 1.0 38497 loop local dist gaussian",
    "comm_modify         vel yes",
    "fix         mvv     all mvv/dpd 0.65",
    "dump        mydump  all atom 100 from_py.lammpstrj",
    "timestep            0.01"
]

lmp.commands_list(initial_commands)
lmp.commands_list(create_commands)
lmp.commands_list(pair_commands)
lmp.commands_list(sim_commands)



lmp.command("run 20")

MPI.Finalize()

print(wave_length)
