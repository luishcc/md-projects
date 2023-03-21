#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_CONCENTRATION=0.5
MAX_CONCENTRATION=3.0
CONCENTRATION_STEP=0.1

N_CPU=4   # For each simulation
N_MAX=3   # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for con in $(seq ${MIN_CONCENTRATION} ${CONCENTRATION_STEP} ${MAX_CONCENTRATION})
do

    mkdir $con
    mpirun -n $N_CPU lmp_py -in surface.lmp -var sc $con > $con/bash.out &
    echo "Running simulation with sc=$con"
    echo
    if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi

done

wait
