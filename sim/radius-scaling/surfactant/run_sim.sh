#!/bin/bash

MIN=1
MAX=20
STEP=1

SC=$1

mkdir $SC

N_CPU=4   # For each simulation
N_MAX=2   # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for con in $(seq ${MIN} ${STEP} ${MAX} )
do

    mkdir $SC/$con
    mpirun -np $N_CPU lmp -in run.lmp -var dir $con sc $SC > $SC/$con/bash.out &
    echo "Running simulation $con with sc = $SC"
    echo
    if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi

done
wait

