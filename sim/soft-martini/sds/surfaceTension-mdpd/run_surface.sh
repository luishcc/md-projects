#!/bin/bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_CONCENTRATION=0.0
MAX_CONCENTRATION=3.0
CONCENTRATION_STEP=0.1

N_CPU=4   # For each simulation
N_MAX=5   # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for con in $(seq ${MIN_CONCENTRATION} ${CONCENTRATION_STEP} ${MAX_CONCENTRATION})
do

    echo "Computing surface density with sc=$con"
    python3 density.py $con
    echo
    if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi

done

wait
