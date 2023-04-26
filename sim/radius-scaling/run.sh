#!/bin/bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

N_MIN=1
N_MAX=10
N_STEP=1

N_CPU=4   # For each simulation
N_MAX=3   # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for con in $(seq ${N_MIN} ${N_MAX} ${N_STEP})
do
    mkdir $con
    mpirun -np $N_CPU lmp -in in.thread.lmp -var rseed $con > $con/bash.out &
    echo "Running simulation $con "
    echo
    if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi
done
wait

