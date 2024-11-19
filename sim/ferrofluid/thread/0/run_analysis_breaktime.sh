#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8


MIN_NS=1
MAX_NS=10
NS_STEP=1


for ns in $(seq ${MIN_NS} ${NS_STEP} ${MAX_NS})
do
      
#  DIR="dip/$ns"
  DIR="free/$ns"

  if [ ! -d "$DIR" ]; then
    echo "$DIR does not exist."
    continue
  fi
      
  if [ -f "$DIR/breaktime.txt" ]; then
    echo "$DIR/breaktime.txt already exists."
    continue
  fi

  echo "Running analysis on $DIR"
  python3 break.py $DIR   
  echo

done


