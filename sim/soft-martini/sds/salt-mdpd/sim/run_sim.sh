#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_CONCENTRATION=1.6
MAX_CONCENTRATION=1.8
CONCENTRATION_STEP=0.2

N_CPU=4   # For each simulation
N_MAX=2  # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for con in 1.0 2.0 4.0 6.0
do

    mkdir $con
    mpirun -n $N_CPU lmp -in surface.lmp -var sc $con > $con/bash.out &
    echo "Running simulation with sc=$con"
    echo
    if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi

done

wait
