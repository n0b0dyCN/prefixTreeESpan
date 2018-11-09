#!/bin/bash
set -ex

sup=('0.1' '0.05' '0.01')
for file in ./treedata/*.data
do
    for s in ${sup[@]}
    do
        python prefixTreeESpan.py -i $file -o out/`basename $file`-$s -m $s
    done
done