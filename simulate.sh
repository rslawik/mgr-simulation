#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

echo "Model: $1"

INJECT_TMP="/tmp/inject.$$.tmp"
echo "Generating $3 packet(s) using $2 generator"
./generate.py $2 $3 $1 >$INJECT_TMP

SIMULATION_TMP="/tmp/simulate.$$.tmp"
echo "Running $4 against $5"
./simulate.py $4 $5 $INJECT_TMP $1 >$SIMULATION_TMP

T=$(./stat.py $SIMULATION_TMP)
echo "Throughput $T"

trap "rm $INJECT_TMP $SIMULATION_TMP" EXIT
