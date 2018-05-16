#!/bin/bash
echo $1
basename=$1


module load bioinfo-tools
module load plink


grep -P "\tI" $basename>> variants_to_remove
grep -P  "\tD" $basename>> variants_to_remove

grep -P "\tA\tT" $basename>> variants_to_remove
grep -P "\tT\tA" $basename>> variants_to_remove
grep -P "\tC\tG" $basename>> variants_to_remove
grep -P "\tG\tC" $basename>> variants_to_remove

plink --bfile $basename --exclude variants_to_remove --make-bed --out ./${basename}_cleaned

