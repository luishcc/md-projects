#!/bin/bash

mpirun -np 2 lmp_py -in run.lmp -var rand $1 
