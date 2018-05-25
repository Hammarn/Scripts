#!/bin/bash

module load bioinfo-tools plink

plink --bfile $1 --genome --out ${1}g
sed  "s/  / /g" ${1}g.genome | sed  "s/  / /g" | sed  "s/  / /g" | sed  "s/  / /g" |  sed  "s/^ //g" | sed  "s/ /\t/g" > genome_sorted_${1}
awk '{print $10}' genome_sorted_${1} > IBSvalues_${1}
