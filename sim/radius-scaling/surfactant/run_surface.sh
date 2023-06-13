#!/bin/bash

MIN=1
MAX=20
STEP=1

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

SC=2.3

N_MAX=4   # N_MAX < 16 (maximum number of cores on office machine)

for con in $(seq ${MIN} ${STEP} ${MAX} )
do

    cd $SC/$con 
    file=$(find . -maxdepth 1 -name "*.lammpstrj" -type f -printf '%f' | head -n1)
    cd ../..
    python3 get_surface.py $SC/$con $file &
    echo "Getting surface profile from simulation $con "
    echo
    if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi

done
wait

