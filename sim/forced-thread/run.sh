#!/usr/bin/env bash


printf "\nRunning sim\n"

mpirun -np 8 python3 ini-test.py
python3 pert-test.py
#mpirun -np 8 lmp < in.tt
