#!/usr/bin/env bash

moltemplate.sh -nocheck -atomstyle "hybrid angle charge" system.lt -xyz $1

rm -rf output_ttree system.in.* run.in.EXAMPLE
