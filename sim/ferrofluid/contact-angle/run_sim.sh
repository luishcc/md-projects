#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_CONCENTRATION=0.05
MAX_CONCENTRATION=0.15
CONCENTRATION_STEP=0.05

MIN_DIPOLE=0.0
MAX_DIPOLE=3.0
DIPOLE_STEP=0.25

MIN_WALL=2
MAX_WALL=8
WALL_STEP=2


N_CPU=4   # For each simulation
N_MAX=3   # N_MAX * N_CPU < 16 (maximum number of cores on office machine)

for con in $(seq ${MIN_CONCENTRATION} ${CONCENTRATION_STEP} ${MAX_CONCENTRATION})
do
  mkdir $con

  for wall in $(seq ${MIN_WALL} ${WALL_STEP} ${MAX_WALL})
  do
    mkdir $con/$wall
    
    for dip in $(seq ${MIN_DIPOLE} ${DIPOLE_STEP} ${MAX_DIPOLE})
    do
      
      DIR=$con/$wall/$dip
      mkdir $DIR
      
      mpirun -n $N_CPU lmp_py -in angle.lmp -var DIR $DIR -var wall $wall -var dip $dip -var con $con > $DIR/bash.out &
      echo "Running simulation on $DIR"
      echo
      if [[ $(jobs -r -p | wc -l) -ge $N_MAX ]]; then wait -n; fi
      
    done
  done
done

wait
