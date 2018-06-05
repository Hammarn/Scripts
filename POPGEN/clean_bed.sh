#!/bin/bash
echo $1
basename=${1%.*}
echo $basename
module load bioinfo-tools
module load plink


grep -P "\tI" ${basename}.bim >> variants_to_remove
grep -P  "\tD" ${basename}.bim >> variants_to_remove

grep -P "\tA\tT" ${basename}.bim >> variants_to_remove
grep -P "\tT\tA" ${basename}.bim >> variants_to_remove
grep -P "\tC\tG" ${basename}.bim >> variants_to_remove
grep -P "\tG\tC" ${basename}.bim >> variants_to_remove

plink --bfile $basename --exclude variants_to_remove --make-bed --out ./${basename}_cleaned

