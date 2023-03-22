#!/bin/bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

SC_LIST="1.0 1.6 2.0 2.3 2.6"

for sc in $SC_LIST; do

    echo "Computing surface density with sc=$sc"
    python3 avg_correlation_z.py $sc

done
