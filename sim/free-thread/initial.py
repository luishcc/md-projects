from mpi4py import MPI
from lammps import lammps
import numpy as np
import sys


radius = int(sys.argv[1])
ratio = int(sys.argv[2])

radius*=0.8

length = radius * ratio * 2 * np.pi
box_sides = radius * np.cbrt(1.5*ratio*np.pi) + 2

seed = int(sys.argv[3])

A = int(sys.argv[4])
B = 25
density = float(sys.argv[5])

save_dir = sys.argv[6]

lmp = lammps('py')

initial_commands = [
    "units lj",
    "dimension 3",
    "boundary p p p",
    "neighbor 0.3 bin",
    "neigh_modify every 1 check yes",
    "atom_style  mdpd",
    "processors 2 1 *"
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


#lmp.command("run 15000")

lmp.command(f"dump mydump all atom 100 {save_dir}/thread.lammpstrj")
lmp.command("dump_modify mydump scale no")

#lmp.command(f"dump force all custom 100 {save_dir}/dump.force id fx fy fz")
#lmp.command(f"dump vels all custom 100 {save_dir}/dump.velocity id vx vy vz")


lmp.command(f"run {sys.argv[7]}")
lmp.command(f"write_restart {save_dir}/restart.thread")


# MPI.Finalize()
