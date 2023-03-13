#!/usr/bin/env bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

MIN_CONCENTRATION=0.1
MAX_CONCENTRATION=3.0
CONCENTRATION_STEP=0.1

AREA=400

for con in $(seq ${MIN_CONCENTRATION} ${CONCENTRATION_STEP} ${MAX_CONCENTRATION})
do
    mkdir $con

    cp surfactant.* $con
    cp system.lt $con
    cd $con


    N=$(echo "scale=0; ($con * $AREA)/1" | bc)
    N2=$(echo "scale=0; $N * 2" | bc)

    echo $N $N2
    TOL=$(echo "scale=1;  2*sqrt( $AREA /(3 * $N )) " | bc)
    echo $TOL

    sed "s/SC/$N/g" -i surfactant.inp
    sed "s/TOL/$TOL/g" -i surfactant.inp
    sed "s/SC/$N2/g" -i system.lt

    packmol < surfactant.inp

    moltemplate.sh -nocheck -atomstyle "hybrid angle charge" system.lt -xyz surf.xyz
    rm -rf output_ttree system.in.* run.in.EXAMPLE

    cd ../
done
