#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_amp=5
MAX_amp=25
amp_STEP=5

MIN_NS=1
MAX_NS=5
NS_STEP=1

for amp in $(seq ${MIN_amp} ${amp_STEP} ${MAX_amp})
do

  for nd in 2 4 8 16
  do
    
    for ns in $(seq ${MIN_NS} ${NS_STEP} ${MAX_NS})
    do
      
      DIR=$amp/$nd/$ns

      if [ ! -d "$DIR" ]; then
        echo "$DIR does not exist."
        continue
      fi

      echo "Running analysis on $DIR"
      python3 break.py $DIR   
      echo

      
    done
  done
done


