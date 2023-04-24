#!/bin/bash 

moltemplate.sh -xyz $1.xyz -atomstyle "hybrid angle charge" -nocheck system.lt
mv system.data $1.data

rm -rf output_ttree
rm -rf run.in.EXAMPLE
rm -rf system.in.*