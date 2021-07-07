from mpi4py import MPI
from lammps import lammps
import numpy as np


radius = 10
radius_init = 1.5*radius
wave_number = 0.55
wave_length = (2 * np.pi * radius) / wave_number

seed = 38497

A = -50
B = 25
density = 6.9


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
    f"region  mdpd  block -{2*radius} {2*radius} -{2*radius} {2*radius} 0 {wave_length} units box",
    "create_box 1 mdpd",
    f"lattice  fcc {density}",
    f"region tube cylinder z 0 0 {radius_init} INF INF",
    "create_atoms  1 region tube",
    "mass 1 1.0"
]

pair_commands = [
    "pair_style hybrid/overlay mdpd/rhosum mdpd 1.0 1.0 9872598",
    "pair_coeff 1 1 mdpd/rhosum  0.75",
    f"pair_coeff 1 1 mdpd {A} {B} 18.0 1.0 0.75"
]

sim_commands = [
    "compute             mythermo all temp",
    f"velocity           all create 1.0 {seed} loop local dist gaussian",
    "comm_modify         vel yes",
    "fix          mvv    all mvv/dpd 0.65",
    "timestep            0.01"
]

lmp.commands_list(initial_commands)
lmp.commands_list(create_commands)
lmp.commands_list(pair_commands)
lmp.commands_list(sim_commands)

lmp.command("run 500")
lmp.command("minimize 0.0 1.0e-8 10000 100000")
lmp.command("write_dump all atom dump.atom modify scale no")

MPI.Finalize()

print('testing')
