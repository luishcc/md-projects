#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_CONCENTRATION=0.05
MAX_CONCENTRATION=0.15
CONCENTRATION_STEP=0.05

MIN_DIPOLE=0.00
MAX_DIPOLE=3.00
DIPOLE_STEP=0.25

MIN_WALL=2
MAX_WALL=8
WALL_STEP=2

for con in $(seq ${MIN_CONCENTRATION} ${CONCENTRATION_STEP} ${MAX_CONCENTRATION})
do

  for wall in $(seq ${MIN_WALL} ${WALL_STEP} ${MAX_WALL})
  do
    
    for dip in $(seq ${MIN_DIPOLE} ${DIPOLE_STEP} ${MAX_DIPOLE})
    do
      
      DIR=$con/$wall/$dip
      if [ ! -d "$DIR" ]; then
        echo "$DIR does not exist."
        continue
      fi

      echo "Running analysis on $DIR"
      python3 analysis.py $DIR   
      echo

      
    done
  done
done


