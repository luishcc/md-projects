#!/bin/bash

end_id=$2
begin_id=$1

while [ $begin_id -le $end_id ]
do
    mkdir $begin_id
    cp run.lmp $begin_id/
    cp run.sh $begin_id/
    cd $begin_id/
    ./run.sh $begin_id
    cd ..
    ((begin_id++))
done
