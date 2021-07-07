from mpi4py import MPI
from lammps import lammps
import numpy as np


radius = 2       # Add as sys.input
ratio = .7       # Add as sys.input , linear instability when > 1 (Continuum Theory)
                 # instability above 0.8 (MDPD Simulation)

length = radius * ratio * 2 * np.pi
box_sides = radius * np.cbrt(1.5*ratio*np.pi) + 2

seed = 38497      # Add as sys.input

A = -50           # Add as sys.input
B = 25
density = 7.0     # Add as sys.input


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
    f"region  mdpd  block -{box_sides} {box_sides} -{box_sides} {box_sides} 0 {length} units box",
    "create_box 1 mdpd",
    f"lattice  fcc {density}",
    f"region tube cylinder z 0 0 {radius} INF INF",
    "create_atoms  1 region tube",
    "mass 1 1.0"
]

pair_commands = [
    "pair_style hybrid/overlay mdpd/rhosum mdpd 1.0 1.0 9872598",
    "pair_coeff 1 1 mdpd/rhosum  0.75",
    f"pair_coeff 1 1 mdpd {A} {B} 18.0 1.0 0.75"
]

thermo_commands = [
    "compute             mythermo all temp",
    "thermo              100",
    "thermo_modify       temp mythermo",
    "thermo_modify       flush yes"
]

sim_commands = [
    f"velocity           all create 1.0 {seed} loop local dist gaussian",
    "comm_modify         vel yes",
    "fix           mvv   all mvv/dpd 0.65",
    "timestep            0.01"
]

lmp.commands_list(initial_commands)
lmp.commands_list(create_commands)
lmp.commands_list(pair_commands)
lmp.commands_list(thermo_commands)
lmp.commands_list(sim_commands)

lmp.command("dump mydump all atom 100 thread3.lammpstrj")
lmp.command("dump_modify mydump scale no")

# lmp.command("dump force all custom 100 dump.thread.custom.dump id vx vy vz fx fy fz")

lmp.command("run 150000")


# MPI.Finalize()
