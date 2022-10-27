#!/usr/bin/bash

# This works too
#if [ $# -ge 1 ]; then
if (( $# >= 1 )); then
    let num=$1
else
    let num=1
fi

upStr="./"
for i in $(seq $num); do
    upStr="$upStr/.."
done

# This also works
#let i=0
#while (( $i < $num )); do
#    upStr=$upStr/..;
#    let i=$((i+1));
#    echo $i
#done

pushd $upStr
