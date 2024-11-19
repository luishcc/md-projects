#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_NS=1
MAX_NS=5
NS_STEP=1

N_CPU=2   # For each simulation

for ns in $(seq ${MIN_NS} ${NS_STEP} ${MAX_NS})
do
      
  DIR="free/$ns"
  mkdir $DIR
      
  mpirun -n $N_CPU lmp_py -in thread2.lmp -var DIR $DIR -var dip 0 -var seed $ns > $DIR/bash.out 
  echo "Running simulation on $DIR"
  echo

done


